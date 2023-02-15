from ..callbacks.callback import Request
from dataclasses import dataclass
from typing import List, Protocol, runtime_checkable


@dataclass
class Result:
    url: str
    status_code: int


@runtime_checkable
class AsyncCrawler(Protocol):
    async def start(self,
                    url: str,
                    ignore_path: List[str]) -> List[Result]:
        pass

    async def fetch_links(self,
                          raw_html: bytes,
                          prev_url: str) -> List[Request]:
        pass
