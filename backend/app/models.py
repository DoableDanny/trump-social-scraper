from sqlalchemy import BigInteger, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from .database import Base

from sqlalchemy.orm import relationship


class Truth(Base):
    __tablename__ = "truths"
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(BigInteger, unique=True, nullable=False)  # API id
    content = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    url = Column(String, unique=True, nullable=False)
    media_attachments = Column(JSONB, nullable=True)

    summary = relationship("TruthSummary", uselist=False, back_populates="truth")


class TruthSummary(Base):
    __tablename__ = "truth_summaries"
    id = Column(Integer, primary_key=True, index=True)
    truth_id = Column(
        Integer, ForeignKey("truths.id", ondelete="CASCADE"), nullable=False
    )
    summary = Column(Text, nullable=False)

    truth = relationship("Truth", back_populates="summary")
