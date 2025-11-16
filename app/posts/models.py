from datetime import datetime
from .. import db
import enum

from sqlalchemy import (
    Integer, String, Text, DateTime, 
    Boolean, Enum, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

class PostCategory(enum.Enum):
    news = 'news'
    publication = 'publication'
    tech = 'tech'
    other = 'other'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    content = db.Column(db.Text, nullable=False)

    posted = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.Column(db.Enum(PostCategory))

    is_active = db.Column(db.Boolean, default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r})"

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"