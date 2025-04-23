from openai import AsyncOpenAI
import os
import re

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def generate_summary(content: str) -> str:
    # Strip HTML tags and check if it's basically empty
    text_only = re.sub(r"<[^>]*>", "", content).strip()
    if not text_only:
        print("No content in truth, so not generating ai summary")
        return ""  # Early return if there's no real content

    try:
        prompt = f"Summarize this social media post in one sentence:\n\n{content}"
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
        )
        summary: str = response.choices[0].message.content or ""
        print("Generated summary")
        print(summary)
        return summary.strip()
    except Exception as e:
        print(f"Summary generation failed: {e}")
        return ""  # fallback to empty string
