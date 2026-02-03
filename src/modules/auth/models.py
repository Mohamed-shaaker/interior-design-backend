from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class User(Base):
    # 1. Responsibility: Table Naming
    __tablename__ = "users"
    
    # 2. Responsibility: Identity
    # id: Mapped[int] ensures Python knows it's an integer.
    # primary_key=True tells the DB this is the unique identifier for every row.
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # 3. Responsibility: Unique Credentials
    # String(255) limits size for performance and indexing.
    # index=True makes searching by email much faster.
    email: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        index=True, 
        nullable=False
    )
    
    # 4. Responsibility: Sensitive Data
    # We never store raw passwords. hashed_password stores the encrypted string.
    hashed_password: Mapped[str] = mapped_column(
        String(555), 
        nullable=False
    )
    
    # 5. Responsibility: Authorization State
    # Boolean maps to the DB 'bool' type.
    # default=True handles the logic when a new user is created.
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True, 
        nullable=False
    )
    
    is_admin: Mapped[bool] = mapped_column(
        Boolean, 
        default=False, 
        nullable=False
    )