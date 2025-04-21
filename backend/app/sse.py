from fastapi import Request
from fastapi.responses import StreamingResponse
import asyncio

subscribers = set()

async def event_generator():
    queue = asyncio.Queue()
    subscribers.add(queue)
    try:
        while True:
            data = await queue.get()
            yield f"data: {data}\n\n"
    finally:
        subscribers.remove(queue)

async def push_event(data):
    for queue in subscribers:
        await queue.put(data)

async def sse_endpoint():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
