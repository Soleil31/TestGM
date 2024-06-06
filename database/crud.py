import logging
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import date

from database.core import AsyncSessionManager
from database.models import TokenBlacklistOutstanding, User
from app.exceptions.user_exceptions import UserAlreadyExists, UserExistError, UnmatchedPassOrUsername


async def create_refresh_token(
        token: str,
        exp: int,
        iat: int,
        jti: str,
        user_id: int
) -> TokenBlacklistOutstanding:
    async with AsyncSessionManager() as session:
        async with session.begin():
            refresh_token = TokenBlacklistOutstanding(
                token=token,
                exp=exp,
                iat=iat,
                jti=jti,
                user_id=user_id
            )
            session.add(refresh_token)
        await session.commit()

        return refresh_token


async def read_user_by_user_id(user_id: int) -> User | None:
    async with AsyncSessionManager() as session:
        statement = select(User).filter_by(id=user_id)
        result = await session.execute(statement=statement)

        user = result.scalars().first()

        if user is None:
            raise UserExistError()

        return user


async def read_user_by_username(username: str) -> User | None:
    async with AsyncSessionManager() as session:
        statement = select(User).filter_by(username=username)
        result = await session.execute(statement=statement)

        user = result.scalars().first()

        if user is None:
            raise UnmatchedPassOrUsername()

        return user


async def create_user(
        username: str,
        email: str,
        hashed_password: str,
        birthday: date = None
) -> User:
    async with AsyncSessionManager() as session:
        try:

            async with session.begin():
                user = User(
                    username=username,
                    email=email,
                    hashed_password=hashed_password,
                    birthday=birthday
                )
                session.add(user)
            await session.commit()

        except IntegrityError as e:
            logging.error(f"Пользователь уже существует: {e}")
            raise UserAlreadyExists()

        return user
