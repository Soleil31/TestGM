import logging
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import date

from database.core import AsyncSessionManager
from database.models import TokenBlacklistOutstanding, User, Subscribe
from app.exceptions.user_exceptions import (
    UserAlreadyExists, UserExistError, UnmatchedPassOrUsername,
    SubscriptionAlreadyExists, SubscriptionDoesNotExist
)
from app.schemas.user_schemas import UserBaseSchema, UserSchema, ListUsersSchema


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


async def read_user_by_user_id(user_id: int) -> UserSchema:
    async with AsyncSessionManager() as session:
        statement = select(User).options(joinedload(User.followers), joinedload(User.following)).filter_by(id=user_id)
        result = await session.execute(statement=statement)

        user = result.scalars().first()

        if user is None:
            raise UserExistError()

        user = UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            followers=[
                UserBaseSchema(
                    id=follower.id,
                    username=follower.username,
                    email=follower.email
                ) for follower in user.followers
            ],
            following=[
                UserBaseSchema(
                    id=followed.id,
                    username=followed.username,
                    email=followed.email
                ) for followed in user.following
            ],
        )

        return user


async def read_user_by_username(username: str) -> User:
    async with AsyncSessionManager() as session:
        statement = select(User).filter_by(username=username)
        result = await session.execute(statement=statement)

        user = result.scalars().first()

        if user is None:
            raise UnmatchedPassOrUsername()

        return user


async def read_list_of_users() -> ListUsersSchema:
    async with AsyncSessionManager() as session:
        statement = select(User).order_by(User.id)
        result = await session.execute(statement=statement)

        users = result.scalars().all()

        users = ListUsersSchema(
            users=[
                UserBaseSchema(
                    id=user.id,
                    username=user.username,
                    email=user.email
                ) for user in users
            ]
        )

        return users


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


async def create_follow_user(
        current_user_id: int,
        following_user_id: int
) -> Subscribe:

    async with AsyncSessionManager() as session:

        try:

            async with session.begin():

                subscribe = Subscribe(
                    follower_id=current_user_id,
                    followed_id=following_user_id
                )
                session.add(subscribe)

            await session.commit()

        except IntegrityError as e:
            logging.error(f"Вы уже подписаны на данного пользователя!: {e}")
            raise SubscriptionAlreadyExists()

        return subscribe


async def delete_follow_user(
        current_user_id: int,
        following_user_id: int
) -> None:

    async with AsyncSessionManager() as session:

        async with session.begin():

            statement = select(Subscribe).filter_by(
                follower_id=current_user_id,
                followed_id=following_user_id
            )
            result = await session.execute(statement)
            subscribe = result.scalars().first()

            if subscribe is None:
                raise SubscriptionDoesNotExist()

            await session.delete(subscribe)

        await session.commit()
