from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base

class GradingResultModel(Base):
    __tablename__ = "grading_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    correct = Column(Integer)
    false = Column(Integer)
    grade = Column(Integer)
    timestamp = Column(DateTime)
