from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func
from sqlalchemy import BigInteger, String, DateTime, Date, ForeignKey
from datetime import datetime, date
from pydantic import EmailStr


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String(30),
        unique=True
    )
    email: Mapped[EmailStr] = mapped_column(
        String,
        unique=True
    )
    hashed_password: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    updated_date: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    birthday: Mapped[date] = mapped_column(
        Date
    )

    followers: Mapped[list["User"]] = relationship(
        "User",
        secondary="subscribe",
        primaryjoin="User.id == Subscribe.followed_id",
        secondaryjoin="User.id == Subscribe.follower_id",
        backref="following"
    )

    notification_settings: Mapped["Notification"] = relationship(
        "Notification",
        back_populates="user",
        uselist=False
    )


class Subscribe(Base):
    __tablename__ = 'subscribe'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    follower_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "user.id",
            ondelete="CASCADE"
        )
    )
    followed_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "user.id",
            ondelete="CASCADE"
        )
    )


class Notification(Base):
    __tablename__ = 'notification'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            'user.id',
            ondelete='CASCADE'
        )
    )
    notification_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    user = relationship(
        'User',
        back_populates='notification_settings'
    )


class TokenBlacklistOutstanding(Base):
    __tablename__ = "token_blacklist_outstanding"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    token: Mapped[str]
    exp: Mapped[int]
    iat: Mapped[int]
    jti: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "user.id",
            ondelete="CASCADE"
        )
    )

    blacklisted_tokens: Mapped[list["TokenBlacklisted"]] = relationship(
        "TokenBlacklisted",
        back_populates="outstanding_token"
    )


class TokenBlacklisted(Base):
    __tablename__ = "token_blacklisted"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )
    blacklisted_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    token_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "token_blacklist_outstanding.id",
            ondelete="CASCADE"
        )
    )

    outstanding_token: Mapped["TokenBlacklistOutstanding"] = relationship(
        "TokenBlacklistOutstanding",
        back_populates="blacklisted_tokens"
    )
