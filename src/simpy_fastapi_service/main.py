import logging.config
import os
import sys
from pathlib import Path

import yaml

from simpy_fastapi_service.app import get_app
from simpy_fastapi_service.settings import get_settings
from simpy_fastapi_service.config.celery_utils import create_celery


# Setting up the application logger
logging_conf = os.getenv("LOGGER_CONF", Path(__file__).parent / "logging.yaml")
with open(logging_conf, "rt") as f:
    log_config = yaml.safe_load(f)
logging.config.dictConfig(log_config)


settings = get_settings()
app = get_app(settings=settings)
app.celery_app = create_celery()
celery = app.celery_app

if __name__ == "__main__":
    """Running with async sqlalchemy in Windows causes issues. Therefore run this script to start uvicorn
    instead of `uvicorn src.simpy_fastapi_service.main:app"""
    import uvicorn

    if sys.platform == "win32" or sys.platform == "win64":
        import asyncio

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    host = os.environ.get("HOST", default="127.0.0.1")
    port = os.environ.get("PORT", default=8080)
    uvicorn.run(app, host=host, port=int(port))
