from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from asyncio import Task

import asyncio
import functools
import sys


class Source(str, Enum):
    FORM = 'form'
    HREF = 'href'


class Method(str, Enum):
    GET = 'get'
    PUT = 'put'
    POST = 'post'
    HEAD = 'head'
    PATCH = 'patch'
    DELETE = 'delete'
    UNKNOWN = 'unknown'

    @classmethod
    def _missing_(cls, value: object) -> 'Method':
        if value is None or not isinstance(value, str):
            return cls.UNKNOWN

        for member in cls:
            if member.value == value.strip().lower():
                return member

        return cls.UNKNOWN


@dataclass
class Request:
    url: str
    source: Source
    method: Method
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Params:
    request: Request
    status_code: Optional[int]
    raw_html: Optional[bytes]


CallbackFunc = Callable[..., Any]


class CallbackLogger:
    def __init__(self, name: str) -> None:
        self.__name = name

    def info(self, message: str) -> None:
        print(f"{self.__name}: [+]", message, file=sys.stdout)

    def warning(self, message: str) -> None:
        print(f"{self.__name}: [-]", message, file=sys.stderr)

    def error(self, message: str) -> None:
        print(f"{self.__name}: [!]", message, file=sys.stderr)


class Callback:
    def __init__(self) -> None:
        self._handlers: Dict[str, CallbackFunc] = {}
        self._queue: List[Task] = []

    def register(self,
                 callback: CallbackFunc,
                 name: Optional[str] = None) -> None:
        if not name:
            name = callback.__name__

        is_exist = self._handlers.get(name) is not None

        if is_exist:
            raise RuntimeError(
                f"Callback with name {name} is already registered!"
            )

        self._handlers[name] = self._wraps(callback, name=name)

    def get_handlers(self) -> List[CallbackFunc]:
        return [callback for callback in self._handlers.values()]

    def handle(self, params: Params) -> None:
        loop = asyncio.get_event_loop()

        for handler in self._handlers.values():
            task = loop.create_task(handler(params))
            self._queue.append(task)

    def get_queues(self) -> List[Task]:
        return self._queue

    async def wait_for_callbacks(self) -> None:
        await asyncio.gather(*self._queue)

    def _wraps(self,
               func: CallbackFunc,
               name: Optional[str] = None) -> CallbackFunc:
        @functools.wraps(func)
        def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Task:
            logger = CallbackLogger(name if name else func.__name__)
            return func(*args, logger, **kwargs)

        return wrapper


CallbackHandler = Callback()
