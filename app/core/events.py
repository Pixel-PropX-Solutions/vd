from typing import Callable
import asyncio
from fastapi import FastAPI
from loguru import logger
import sys
from playwright.async_api import async_playwright
from app.database import mongodb
from app.core.services import browser as shared_browser


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore

    @logger.catch
    async def start_app() -> None:
        try:
            if sys.platform.startswith("win"):
                loop = asyncio.ProactorEventLoop()
                asyncio.set_event_loop(loop)
            playwright = await async_playwright().start()
            shared_browser = await playwright.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-gpu",
                    "--disable-software-rasterizer",
                    "--disable-dev-shm-usage",
                    # "--use-gl=swiftshader",  # keep only if needed
                ],
            )
            await mongodb.client.admin.command("ping")
            logger.info("MongoDB Connected.")
        except Exception as e:
            raise e

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore

    @logger.catch
    async def stop_app() -> None:
        try:
            await shared_browser.close()
            mongodb.client.close()
            logger.info("Closed MongoDB Connection")
        except Exception as e:
            raise e

    return stop_app
