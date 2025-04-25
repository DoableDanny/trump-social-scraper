from fastapi import Request
from fastapi.responses import StreamingResponse
import asyncio
import json

subscribers = set()


async def event_generator():
    queue = asyncio.Queue()
    subscribers.add(queue)
    try:
        # Send an initial heartbeat event immediately after connection
        yield "event: heartbeat\ndata: connected\n\n"

        while True:
            data = await queue.get()
            json_data = json.dumps(data, default=str)
            print("Sending SSE:", f"data: {json_data}")
            yield f"data: {json_data}\n\n"
    finally:
        subscribers.remove(queue)


async def push_event(data):
    for queue in subscribers:
        await queue.put(data)


async def sse_endpoint():
    response = StreamingResponse(event_generator(), media_type="text/event-stream")
    response.headers["Access-Control-Allow-Origin"] = (
        "https://trump-social-scraper.netlify.app"
    )
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = (
        "no"  # Disable buffering for nginx if you're behind nginx
    )
    return response
