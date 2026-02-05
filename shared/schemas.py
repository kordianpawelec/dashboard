from typing import Optional
from sqlalchemy import String, create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped, Session
from datetime import datetime
import uuid


class Base(DeclarativeBase):
    pass


engine = create_engine("sqlite:///dashboard.db", echo=True)

def init_db():
    Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = "user_account"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)
    
    storage_files: Mapped[list["Storage"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class Storage(Base):
    __tablename__ = "storage"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    user: Mapped["User"] = relationship(back_populates="storage_files")

    def __repr__(self) -> str:
        return f"Storage(id={self.id}, filename={self.filename}, user_id={self.user_id})"


class DBController:
    def __init__(self, session: Session = None):
        self.session = session
    
    def add_user(self, user: User) -> User:
        """Add a new user to database"""
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
    
    def get_user_by_token(self, token: str) -> Optional[User]:
        """Get user by token"""
        with Session(engine) as session:
            return session.query(User).filter(User.token == token).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        with Session(engine) as session:
            return session.query(User).filter(User.username == username).first()
    
    def close(self):
        if self.session:
            self.session.close()

