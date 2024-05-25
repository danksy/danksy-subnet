import datetime
import json
import os
import sys

from loguru import logger


def iso_timestamp_now() -> str:
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    iso_now = now.isoformat()
    return iso_now


def _serialize(record):
    subset = {
        "timestamp": record["time"].timestamp(),
        "message": record["message"],
        "level": record["level"].name,
        "location": f'{record["file"]}:{record["line"]}',
        "extra": record["extra"],
    }
    return json.dumps(subset)


def _patching(record):
    record["extra"]["serialized"] = _serialize(record)


log_mode = os.getenv("LOG_MODE", "console")
match log_mode:
    case "json":
        logger.remove()
        logger = logger.patch(_patching)
        logger.add(sys.stderr, format="{extra[serialized]}")
    case _:
        logger.remove()
        logger.add(sys.stdout, colorize=True, format="{time} | {level} | {file}:{line} | {extra} | {message}")

logger = logger
