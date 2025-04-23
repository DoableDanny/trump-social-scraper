from typing import Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .models import Truth, TruthSummary
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
        "media_attachments": truth.media_attachments,
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


async def create_summary(db: AsyncSession, truth_id: int, summary_text: str):
    try:
        summary = TruthSummary(truth_id=truth_id, summary=summary_text)
        db.add(summary)
        await db.commit()
        await db.refresh(summary)
        return summary
    except Exception as e:
        await db.rollback()
        print(f"Failed to create summary for truth {truth_id}: {e}")
        return None
