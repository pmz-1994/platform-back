import logging
from django.conf import settings
from fluent import handler

logger = logging.getLogger("platformback")

if settings.FLUENTD_ENABLED:
    logger.setLevel(level=logging.INFO)
    logHandler = handler.FluentHandler(
        settings.FLUENTD_TAG,
        host=settings.FLUENTD_SERVER,
        port=int(settings.FLUENTD_PORT),
        nanosecond_precision=True,
    )
    formatter = handler.FluentRecordFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)


def log_user_connect(func):
    def wrapper(*args, **kwargs):
        user = func(*args, **kwargs)
        logger.info(
            {
                "env": settings.ENV,
                "email": user.email,
                "email_domain": user.email.split("@")[-1],
                "action": "connect_to_platform",
                "message": f"{user.email} has just logged on to the platform",
            }
        )
        return user

    return wrapper


def log_user_first_connection(func):
    def wrapper(*args, **kwargs):
        user = func(*args, **kwargs)
        logger.info(
            {
                "env": settings.ENV,
                "email": user.email,
                "action": "first_connection_to_platform",
                "message": f"{user.email} has logged on to the platform for the first time",
            }
        )
        return user

    return wrapper
