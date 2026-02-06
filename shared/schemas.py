from typing import Optional
from sqlalchemy import String, create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped, Session
from datetime import datetime, timezone
import uuid


class Base(DeclarativeBase):
    pass


engine = create_engine("sqlite:///dashboard.db", echo=True)

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

class User(Base):
    __tablename__ = "user_account"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(default=True)
    files: Mapped[list["Files"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class Files(Base):
    __tablename__ = 'files'
    
    file_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates='files')
    original_name: Mapped[str] = mapped_column(String(300), nullable=False)
    stored_filename: Mapped[str] = mapped_column(String(300), nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
