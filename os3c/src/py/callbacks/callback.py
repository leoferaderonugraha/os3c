from dataclasses import dataclass
from typing import Any, Callable, List
from asyncio import Task


@dataclass
class Params:
    url: str
    status_code: int
    raw_html: bytes


Callback = Callable[[Params], Any]
CallbackQueue: List[Task] = []
