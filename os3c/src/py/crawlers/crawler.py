from ..callbacks import Callback
from dataclasses import dataclass
from typing import List, Protocol, runtime_checkable


@dataclass
class Result:
    url: str
    status_code: int


@runtime_checkable
class AsyncCrawler(Protocol):
    def __init__(self, callbacks: List[Callback]) -> None:
        pass

    async def start(self,
                    url: str,
                    ignore_path: List[str]) -> List[Result]:
        pass

    async def fetch_links(self, raw_html: bytes) -> List[str]:
        pass
