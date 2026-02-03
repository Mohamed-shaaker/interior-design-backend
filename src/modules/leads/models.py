from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Lead(Base):
  """
  
  """
  __tablename__ = "leads"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  
  full_name: Mapped[str] = mapped_column(String(255), nullable=False)
  
  email: Mapped[str] = mapped_column(String(255), nullable=False)
  
  project_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
  
  description: Mapped[str] = mapped_column(Text, nullable=False)