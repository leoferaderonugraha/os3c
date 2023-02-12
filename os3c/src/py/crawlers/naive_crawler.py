from .crawler import AsyncCrawler, Result
from ..callbacks import Callback, Params, CallbackQueue

from selectolax.parser import HTMLParser
from typing import List, Set
from urllib.parse import urlsplit, SplitResult

import asyncio
import httpx


class NaiveCrawler(AsyncCrawler):
    """Crawl using BFS method"""

    def __init__(self, callbacks: List[Callback]) -> None:
        self._queue: List[str] = []
        self._visited: Set[str] = set()
        self._results: List[Result] = []
        self._client = httpx.AsyncClient()
        self._evt_loop = asyncio.get_event_loop()
        self._callbacks = callbacks

    async def start(self,
                    url: str,
                    ignore_path: List[str] = []) -> List[Result]:
        url_parts: SplitResult = urlsplit(url)
        base_domain: str = url_parts.netloc
        scheme: str = url_parts.scheme

        await self._crawl(url, base_domain, scheme, ignore_path)

        while len(self._queue) > 0:
            queued_url = self._queue.pop(0)
            try:
                await self._crawl(queued_url, base_domain, scheme, ignore_path)
            except (httpx.ConnectError,
                    httpx.ReadTimeout,
                    httpx.ConnectTimeout):
                self._visited.add(url)

        return self._results

    async def fetch_links(self, raw_html: bytes) -> List[str]:
        html = HTMLParser(raw_html)
        links = []

        for link in html.tags('a'):
            href = link.attrs.get('href')
            if href:
                links.append(href.strip())

        return links

    def _is_ignored(self,
                    url: str,
                    ignore_path: List[str]) -> bool:
        for ignore in ignore_path:
            if url.startswith(ignore):
                return True

        return False

    async def _crawl(self,
                     url: str,
                     base_domain: str,
                     scheme: str,
                     ignore_path: List[str] = []) -> None:
        response = await self._client.get(url)
        result = Result(url=url, status_code=response.status_code)

        self._visited.add(url)
        self._results.append(result)

        for callback in self._callbacks:
            params = Params(url=url,
                            status_code=response.status_code,
                            raw_html=response.content)
            task = self._evt_loop.create_task(asyncio.to_thread(callback,
                                                                params))
            CallbackQueue.append(task)

        links = await self.fetch_links(response.content)

        for link in links:
            link_parts: SplitResult = urlsplit(link)

            if self._is_ignored(link_parts.path, ignore_path):
                continue

            if not link_parts.netloc and link_parts.path:
                path = link_parts.path

                if path[0] != '/':
                    path = '/' + link_parts.path

                link = f"{scheme}://{base_domain}{path}"

                if link in self._queue or link in self._visited:
                    continue

                self._queue.append(link)
                self._visited.add(link)
            elif link_parts.netloc == base_domain:
                if link in self._queue or link in self._visited:
                    continue

                self._queue.append(link)
                self._visited.add(link)
