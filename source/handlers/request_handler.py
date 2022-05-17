from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from aiohttp.client_exceptions import ClientResponseError, ClientConnectorError
from source.data_classes.rm_group import RMGroup
from source.data_classes.rm_user import RMUser
from source.data_classes.errors import RequestError


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request):
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: Any):
        if self._next_handler:
            return self._next_handler.handle(request)
        return request


class GroupHandler(AbstractHandler):
    def handle(self, request):
        pass


class RequestErrorHandler(AbstractHandler):
    async def handle(self, request: Any):
        try:
            response = await request()
        except ClientConnectorError as c_c_e:
            raise RequestError.create_unaddressed(str(c_c_e))
        except ClientResponseError as c_r_e:
            raise RequestError.create_unaddressed(f"Resource {c_r_e.message.lower()}.")
        else:
            return super().handle(response)


class GroupDataHandler(AbstractHandler):
    @staticmethod
    def is_valid(data: dict, key) -> bool:
        return key in data

    @staticmethod
    def create_group(data: dict):
        users = [RMUser.create(**user) for user in data["users"]]
        return RMGroup.create_with_users(data["id"], data["name"], users)

    def handle(self, data: Any):
        if self.is_valid(data, "group"):
            return self.create_group(data.get("group"))
        else:
            return super().handle(data)


class UserDataHandler(AbstractHandler):
    @staticmethod
    def is_valid(data: dict, key) -> bool:
        return key in data

    @staticmethod
    def get_hours(data: dict):
        return sum([values["hours"] for values in data["time_entries"]])

    @staticmethod
    def get_comments(data: dict):
        return len(''.join([values["comments"] for values in data["time_entries"]]))

    def handle(self, data: Any):
        if self.is_valid(data, "time_entries"):
            return dict(hours=self.get_hours(data),
                        comments=self.get_comments(data))
        else:
            return super().handle(data)
