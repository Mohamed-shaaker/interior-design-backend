from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import session_factory

async def get_db() -> AsyncGenerator[AsyncSession, None]:
  """
 
  """
  async with session_factory() as session:
    try:
      yield session
    finally:
      await session.close()