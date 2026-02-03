from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

# 1. The Connection String
# The startup success confirms this URL and your password are correct
DATABASE_URL = "postgresql+asyncpg://postgres:982060@localhost:5432/interior_design_db"

# 2. The Engine
# echo=True is currently showing you the SQL magic happening in your terminal
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# 3. The Session Factory
session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# 4. The Base Class and Mixins
class Base(DeclarativeBase):
    pass

class TimestampMixin:
    """
    Mixin to add created_at and updated_at columns automatically.
    This helps track when leads or users were created.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        onupdate=func.now(), 
        server_default=func.now()
    )