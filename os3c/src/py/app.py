from .callbacks import Callback, CallbackQueue
from .crawlers.crawler import AsyncCrawler
from typing import List, Type

import asyncio


class App:
    def __init__(self,
                 crawler: Type[AsyncCrawler],
                 callbacks: List[Callback]) -> None:
        self.__crawler: AsyncCrawler = crawler(callbacks=callbacks)
        self.__callbacks = callbacks

    async def check(self,
                    url: str,
                    ignore_path: List[str] = []) -> None:
        _ = await self.__crawler.start(url, ignore_path=ignore_path)

    async def wait_for_callbacks(self) -> None:
        """
        Wait for callback(s) that is still processing
        after the crawler finished.
        """

        await asyncio.gather(*CallbackQueue)
