from aiogram import Bot, Dispatcher, types
from data import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration

sentry_sdk.init(dsn="https://9946c6f40846767c4b2b652c457f13a2@o1341400.ingest.sentry.io/4506044345155584",
                integrations=[AsyncioIntegration()])
