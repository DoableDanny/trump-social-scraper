import contextlib
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright

from .sse import sse_endpoint
from .scraper import scraper_task
from .database import get_db, engine, Base
from .crud import get_latest_external_id, get_latest_truths
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db_gen = get_db()
    db = await anext(db_gen)  # get actual session from generator

    task = asyncio.create_task(scraper_task(db))
    yield

    task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await task

    await db_gen.aclose()  # clean up generator session


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}


@app.get("/truths")
async def get_truths(db: AsyncSession = Depends(get_db)):
    return await get_latest_truths(db)


@app.get("/stream")
async def stream():
    return await sse_endpoint()


@app.get("/latest-truth")
async def latest_truth(db: AsyncSession = Depends(get_db)):
    truth = await get_latest_external_id(db)
    return truth


@app.get("/test-playwright")
async def test_playwright():
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
            """async () => {
            const res = await fetch("https://truthsocial.com/api/v1/accounts/107780257626128497/statuses?exclude_replies=true&only_replies=false&with_muted=true&limit=20&since_id=100", {
                headers: { "Accept": "application/json" }
            });
            return await res.json();
        }"""
        )

        await browser.close()
        return {"count": len(data), "first": data[0] if data else None}
