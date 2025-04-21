from sqlalchemy import BigInteger, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base


class Truth(Base):
    __tablename__ = "truths"
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(BigInteger, unique=True, nullable=False)  # API id
    content = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    url = Column(String, unique=True, nullable=False)
    media_url = Column(String, nullable=True)
