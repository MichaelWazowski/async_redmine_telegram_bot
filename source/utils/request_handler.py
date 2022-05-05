from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from aiohttp.client_exceptions import ClientResponseError, ClientConnectorError


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def validate(self, request):
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def validate(self, request: Any):
        if self._next_handler:
            return self._next_handler.validate(request)
        return request


class RequestErrorHandler(AbstractHandler):
    async def validate(self, request: Any):
        try:
            response = await request()
        except ClientConnectorError as c_c_e:
            return str(c_c_e)
        except ClientResponseError as c_r_e:
            return str(c_r_e)
        else:
            super().validate(response)


class DataErrorHandler(AbstractHandler):
    def validate(self, request: dict):
        if type(request) is dict:
            return request
        else:
            super().validate(request)
