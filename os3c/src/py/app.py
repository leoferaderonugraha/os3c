from .callbacks.callback import CallbackHandler
from .crawlers.crawler import AsyncCrawler
from typing import List


class App:
    def __init__(self, crawler: AsyncCrawler) -> None:
        self.__crawler: AsyncCrawler = crawler

    async def check(self,
                    url: str,
                    ignore_path: List[str] = []) -> None:
        _ = await self.__crawler.start(url, ignore_path=ignore_path)

    async def wait_for_callbacks(self) -> None:
        await CallbackHandler.wait_for_callbacks()
