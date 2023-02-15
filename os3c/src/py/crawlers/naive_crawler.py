from ..callbacks import (
    CallbackHandler, Params,
    Request, Source, Method,
)
from .crawler import AsyncCrawler, Result

from selectolax.parser import HTMLParser
from typing import List
from urllib.parse import urljoin, urlsplit

import httpx


class NaiveCrawler(AsyncCrawler):
    """Crawl using BFS method"""

    def __init__(self) -> None:
        self._queue: List[Request] = []
        self._visited: List[Request] = []
        self._results: List[Result] = []
        self._client = httpx.AsyncClient(follow_redirects=True)

    async def start(self,
                    url: str,
                    ignore_path: List[str] = []) -> List[Result]:
        url_parts = urlsplit(url)
        base_domain = url_parts.netloc
        scheme = url_parts.scheme

        request = Request(url=url, source=Source.HREF, method=Method.GET)

        await self._crawl(request, base_domain, scheme, ignore_path)

        while len(self._queue) > 0:
            queued = self._queue.pop(0)
            try:
                await self._crawl(queued, base_domain, scheme, ignore_path)
            except (httpx.ConnectError,
                    httpx.ReadTimeout,
                    httpx.RemoteProtocolError,
                    httpx.ConnectTimeout):
                self._visited.append(queued)
            except httpx.UnsupportedProtocol:
                print('UnsupportedProtocol:', queued)

        return self._results

    async def fetch_links(self,
                          raw_html: bytes,
                          prev_url: str) -> List[Request]:
        html = HTMLParser(raw_html)
        links = []

        for link in html.tags("a"):
            href = link.attrs.get("href")
            if href:
                href = href.strip()
                if not href:
                    continue

                parts = urlsplit(href)

                if not parts.scheme and not parts.netloc and not parts.path:
                    continue
                elif parts.fragment or parts.scheme == 'mailto':
                    continue

                if not parts.scheme and not parts.netloc:
                    href = urljoin(prev_url, href)

                links.append(Request(url=href,
                                     source=Source.HREF,
                                     method=Method.GET))

        for form in html.tags('form'):
            action = form.attrs.get('action')

            if not action or (action and not action.strip()):
                # Ignore empty form action for now
                continue

            method = form.attrs.get('method')
            form_params = {}

            for param in form.traverse():
                param_name = param.attrs.get('name')

                if param_name is None:
                    continue

                form_params[param_name] = param.attrs.get('type')

            form_request = Request(url=action.strip(),
                                   source=Source.FORM,
                                   method=Method(method),
                                   params=form_params)

            links.append(form_request)

        return links

    def _is_ignored(self,
                    url: str,
                    ignore_path: List[str]) -> bool:
        for ignore in ignore_path:
            if url.startswith(ignore):
                return True

        return False

    async def _crawl(self,
                     request: Request,
                     base_domain: str,
                     scheme: str,
                     ignore_path: List[str] = []) -> None:
        # Skip FORM, call callback(s) instead.
        if request.source is Source.FORM:
            params = Params(request=request,
                            status_code=None,
                            raw_html=None)

            CallbackHandler.handle(params)

            return None

        response = await self._client.get(request.url)
        result = Result(url=request.url,
                        status_code=response.status_code)

        self._visited.append(request)
        self._results.append(result)

        callback_params = Params(request=request,
                                 status_code=response.status_code,
                                 raw_html=response.content)

        CallbackHandler.handle(callback_params)

        requests = await self.fetch_links(response.content, request.url)

        for request in requests:
            request_parts = urlsplit(request.url)

            if self._is_ignored(request_parts.path, ignore_path):
                continue

            if not request_parts.netloc and request_parts.path:
                path = request_parts.path
                request.url = f"{scheme}://{base_domain}{path}"

                if request in self._queue or request in self._visited:
                    continue

                self._queue.append(request)
                self._visited.append(request)
            elif request_parts.netloc == base_domain:
                if request in self._queue or request in self._visited:
                    continue

                self._queue.append(request)
                self._visited.append(request)
