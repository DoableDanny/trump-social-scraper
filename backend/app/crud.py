from typing import Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .models import Truth
from sqlalchemy import select, desc


def format_truth(truth):
    print("This is id")
    print(truth.id)
    return {
        "id": truth.id,
        "external_id": truth.external_id,
        "content": truth.content,
        "timestamp": truth.timestamp.isoformat(),
        "url": truth.url,
        "media_url": truth.media_url,
    }


async def get_latest_truths(db: AsyncSession, limit: int = 20):
    result = await db.execute(
        select(Truth).order_by(Truth.timestamp.desc()).limit(limit)
    )
    return [format_truth(t) for t in result.scalars().all()]


async def get_latest_external_id(db: AsyncSession) -> Optional[int]:
    result = await db.execute(
        select(Truth.external_id).order_by(desc(Truth.external_id)).limit(1)
    )
    latest = result.scalar_one_or_none()
    return latest


async def create_truth(db: AsyncSession, data):
    truth = Truth(**data)
    db.add(truth)
    try:
        await db.commit()
        await db.refresh(truth)
        return truth
    except IntegrityError as e:
        await db.rollback()
        print("Skipping duplicate or failed truth:", e)
        return None
