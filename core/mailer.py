import time
from datetime import datetime
import asyncio

from contextlib import suppress

from aiogram import Bot
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError, TelegramRetryAfter
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import User


class MessageMailer:

    DEFAULT_DELAY = 1/25
    LAST_UPDATE = 0
    TIME_STARTED = 0


    @staticmethod
    def pretty_time(seconds: float) -> str:

        seconds = int(seconds)

        return '%0d:%0d:%0d' % (
            seconds // 3600,
            seconds % 3600 // 60,
            seconds % 60
        )


    @classmethod
    def get_text(cls, scope: list[int], sent: int, delay: float) -> str:

        progress = int(sent / len(scope) * 25)
        progress_bar = ('=' * progress) + (' ' * (25 - progress))

        return "<code>[%s]</code> %s/%s (ETA: %s)" % (
            progress_bar,
            sent,
            len(scope),
            cls.pretty_time((len(scope) - sent) * delay)
        )


    @classmethod
    async def start_mailing(cls, message: Message, scope: list[int], session: AsyncSession, delay: float=None) -> None:

        delay = delay or cls.DEFAULT_DELAY

        time_started = time.time()
        cls.TIME_STARTED = time_started

        blocked = 0
        msg = await message.answer(
            cls.get_text(
                scope, 1, delay,
            ),
            ParseMode.HTML,
        )
        cls.LAST_UPDATE = time.time()

        for sent, user_id in enumerate(scope, 1):

            if time_started != cls.TIME_STARTED:

                break

            if time.time() - cls.LAST_UPDATE > 2:

                cls.LAST_UPDATE = time.time()

                with suppress(TelegramAPIError):
                    
                    await msg.edit_text(
                        cls.get_text(
                            scope, sent, delay,
                        ),
                        ParseMode.HTML,
                    )

            try:

                await message.copy_to(
                    user_id,
                    reply_markup=message.reply_markup,
                )

            except TelegramRetryAfter as exc:

                delay *= 2
                await asyncio.sleep(exc.retry_after)

            except TelegramAPIError:

                blocked += 1
                
                try:
                    await session.execute(update(User).where(User.id==user_id).values(
                    block_date=datetime.utcnow(),
                    active=False
                    ))
                    
                    await session.commit()
                except:
                    pass

            await asyncio.sleep(delay)

        with suppress(TelegramAPIError):

            await msg.edit_text(
                text=cls.get_text(
                    scope, len(scope), delay,
                ),
                parse_mode=ParseMode.HTML
            )

        await msg.answer(
            'Рассылка завершена.\nУспешно: %s.\nБот заблокирован: %s' % (
                len(scope) - blocked,   
                blocked,
            )
        )


class GroupMessageMailer:

    DEFAULT_DELAY = 1/25
    LAST_UPDATE = 0
    TIME_STARTED = 0


    @staticmethod
    def pretty_time(seconds: float) -> str:

        seconds = int(seconds)

        return '%0d:%0d:%0d' % (
            seconds // 3600,
            seconds % 3600 // 60,
            seconds % 60
        )


    @classmethod
    def get_text(cls, scope: list[int], sent: int, delay: float) -> str:

        progress = int(sent / len(scope) * 25)
        progress_bar = ('=' * progress) + (' ' * (25 - progress))

        return "<code>[%s]</code> %s/%s (ETA: %s)" % (
            progress_bar,
            sent,
            len(scope),
            cls.pretty_time((len(scope) - sent) * delay)
        )


    @classmethod
    async def start_mailing(cls,message: Message, bot: Bot, media: list, scope: list[int], 
                            session: AsyncSession, delay: float=None) -> None:

        delay = delay or cls.DEFAULT_DELAY

        time_started = time.time()
        cls.TIME_STARTED = time_started

        blocked = 0
        msg = await message.answer(
            cls.get_text(
                scope, 1, delay,
            ),
            ParseMode.HTML,
        )
        cls.LAST_UPDATE = time.time()

        for sent, user_id in enumerate(scope, 1):

            if time_started != cls.TIME_STARTED:

                break

            if time.time() - cls.LAST_UPDATE > 2:

                cls.LAST_UPDATE = time.time()

                with suppress(TelegramAPIError):
                    
                    await msg.edit_text(
                        cls.get_text(
                            scope, sent, delay,
                        ),
                        ParseMode.HTML,
                    )

            try:
                await bot.send_media_group(user_id, media)
                # await message.copy_to(
                #     user_id,
                #     reply_markup=message.reply_markup,
                # )

            except TelegramRetryAfter as exc:

                delay *= 2
                await asyncio.sleep(exc.retry_after)

            except TelegramAPIError:

                blocked += 1
                
                try:
                    await session.execute(update(User).where(User.id==user_id).values(
                    block_date=datetime.utcnow(),
                    active=False
                    ))
                    
                    await session.commit()
                except:
                    pass

            await asyncio.sleep(delay)

        with suppress(TelegramAPIError):

            await msg.edit_text(
                text=cls.get_text(
                    scope, len(scope), delay,
                ),
                parse_mode=ParseMode.HTML
            )

        await msg.answer(
            'Рассылка завершена.\nУспешно: %s.\nБот заблокирован: %s' % (
                len(scope) - blocked,   
                blocked,
            )
        )
