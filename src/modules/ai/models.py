from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base, TimestampMixin

class DesignAnalysis(Base, TimestampMixin):
    __tablename__ = "design_analyses"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    ai_summary: Mapped[str] = mapped_column(Text)
    suggested_style: Mapped[str] = mapped_column(String(100))