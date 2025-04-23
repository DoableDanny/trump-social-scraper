import asyncio
from datetime import datetime
from typing import Optional

from .ai import generate_summary
from .crud import create_summary, create_truth, format_truth, get_latest_external_id
from .sse import push_event
from sqlalchemy.ext.asyncio import AsyncSession
from playwright.async_api import async_playwright
from playwright.async_api import async_playwright
from datetime import datetime


async def fetch_new_truths(since_id: Optional[int] = None):
    base_url = "https://truthsocial.com/api/v1/accounts/107780257626128497/statuses"
    query = "?exclude_replies=true&only_replies=false&with_muted=true&limit=20"
    if since_id:
        query += f"&since_id={since_id}"

    url = base_url + query
    truths = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                ],
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                locale="en-US",
            )
            page = await context.new_page()
            await page.goto("https://truthsocial.com", wait_until="networkidle")

            data = await page.evaluate(
                f"""async () => {{
                    const response = await fetch("{url}", {{
                        headers: {{
                            "Accept": "application/json"
                        }}
                    }});
                    return await response.json();
                }}"""
            )

            for item in data:
                created_at = item.get("created_at")
                if not created_at:
                    continue

                truths.append(
                    {
                        "external_id": int(item["id"]),
                        "content": item["content"],
                        "timestamp": datetime.fromisoformat(
                            created_at.replace("Z", "+00:00")
                        ),
                        "url": item["url"],
                        "media_attachments": item["media_attachments"],
                    }
                )

            await browser.close()
            return truths

    except Exception as e:
        print(f"Error fetching truths with Playwright: {e}")
        return []


# What should this do?
# This runs in the background.
# Initially, it fetches the first 20 posts from API.
# After that, it fetches later posts from the API.
# The user sees latest 20 posts by hitting /truths
# They can then stream new posts hitting /stream
async def scraper_task(db: AsyncSession):
    while True:
        since_id = await get_latest_external_id(db)
        print("Since this id:")
        print(since_id)
        new_truths = await fetch_new_truths(since_id=since_id)
        print("New truths:")
        print(new_truths)
        for truth in reversed(new_truths):
            try:
                db_truth = await create_truth(db, truth)
                if db_truth:
                    db_summary = await generate_and_save_summary(db, db_truth)
                    formatted = format_truth(db_truth)
                    formatted["ai_summary"] = db_summary.summary if db_summary else ""
                    await push_event(formatted)
            except Exception as e:
                print("Skipping duplicate or failed truth:", e)
        await asyncio.sleep(30)


async def generate_and_save_summary(db, truth):
    print("CONTENT: " + truth.content)
    ai_summary = await generate_summary(truth.content)
    db_summary = None
    if ai_summary:
        print(f"Creating summary in db for truth {truth.id}")
        db_summary = await create_summary(db, truth.id, ai_summary)
    return db_summary
