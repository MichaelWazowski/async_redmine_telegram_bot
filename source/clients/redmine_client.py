import os
from source.clients.http_client import HTTPClient
from source.handlers.request_handler import RequestErrorHandler, GroupDataHandler, UserDataHandler


class RedmineClient:

    @staticmethod
    async def new_session_request(query):
        new_session = HTTPClient()
        return await new_session.make_request(query)

    def __init__(self):
        self.__url = os.getenv("REDMINE_URL")
        self.__token = os.getenv("REDMINE_TOKEN")
        self.request_error_handler = RequestErrorHandler()
        self.group_data_handler = GroupDataHandler()
        self.user_data_handler = UserDataHandler()
        self.request_error_handler.set_next(self.group_data_handler).set_next(self.user_data_handler)

    async def get_redmine_group(self, group_id):
        query = self._get_redmine_group_query(group_id=group_id, include="users")
        return await self.request_error_handler.handle(lambda: self.new_session_request(query))

    async def get_redmine_user_data(self, user_id, start_date, end_date):
        query = self._get_redmine_user_query(user_id=user_id, from_date=start_date, to_date=end_date)
        return await self.request_error_handler.handle(lambda: self.new_session_request(query))

    def _get_redmine_group_query(self, group_id, include=None):
        return "{url}/groups/{group_id}.json?{include}&key={key}".format(
            url=self.__url,
            group_id=group_id,
            include="include={include}".format(include=include) if include else "",
            key=self.__token)

    def _get_redmine_user_query(self, user_id, from_date, to_date):
        return '{url}/time_entries.json?user_id={user_id}&from={from_date}&to={to_date}&key={key}'.format(
            url=self.__url,
            user_id=user_id,
            from_date=from_date,
            to_date=from_date if to_date is None else to_date,
            key=self.__token
        )
