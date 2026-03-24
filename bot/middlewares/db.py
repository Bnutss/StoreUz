import os
import django
from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


class DjangoSetupMiddleware(BaseMiddleware):
    def __init__(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StoreUz.settings')
        django.setup()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        return await handler(event, data)


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        from telegrambot.models import TelegramUser

        tg_user: User | None = data.get('event_from_user')
        if tg_user:
            db_user, _ = await TelegramUser.objects.aget_or_create(
                telegram_id=tg_user.id,
                defaults={
                    'username': tg_user.username or '',
                    'first_name': tg_user.first_name or '',
                    'last_name': tg_user.last_name or '',
                },
            )
            data['db_user'] = db_user
        else:
            data['db_user'] = None

        return await handler(event, data)
