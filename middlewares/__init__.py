from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())


import sentry_sdk
sentry_sdk.init(
    dsn="https://b7cf5fbbf84e448ab4a17cdefa9e7ed8@o4504621259948032.ingest.sentry.io/4505091887988736",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)
