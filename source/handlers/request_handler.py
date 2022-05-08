from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from aiohttp.client_exceptions import ClientResponseError, ClientConnectorError
from source.data_classes.rm_group import RMGroup
from source.data_classes.rm_user import RMUser


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
            return f"Resource {c_r_e.message.lower()}."
        else:
            return super().validate(response)


class GroupDataHandler(AbstractHandler):
    @staticmethod
    def create_group(response: dict):
        response = response[0]
        for key, value in response.items():
            group_data = value.get("group")
            group = RMGroup.create_empty(group_data["id"], group_data["name"])
            for user in group_data["users"]:
                new_user = RMUser.create(**user)
                group.add_users(new_user)
            return group

    def validate(self, request: Any):
        if type(request) == list:
            return self.create_group(request)
        else:
            return super().validate(request)


class UserDataHandler(AbstractHandler):
    @staticmethod
    def get_hours(value):
        return sum([data["hours"] for data in value["time_entries"]])

    @staticmethod
    def get_comments(value):
        return len(''.join([data["comments"] for data in value["time_entries"]]))

    def validate(self, request: Any):
        if type(request) == dict:
            return dict(hours=UserDataHandler.get_hours(request),
                        comments=UserDataHandler.get_comments(request))
        else:
            return super().validate(request)
