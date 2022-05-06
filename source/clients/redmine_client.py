from source.clients.http_client import HTTPClient
from source.handlers.request_handler import RequestErrorHandler, GroupDataHandler, UserDataHandler


class RedmineClient:
    @staticmethod
    async def new_session_request(request_body):
        new_session = HTTPClient()
        return await new_session.make_request(request_body)

    def __init__(self, url: str, token: str):
        self.__url = url
        self.__token = token
        self.request_error_handler = RequestErrorHandler()
        self.group_data_handler = GroupDataHandler()
        self.user_data_handler = UserDataHandler()

    async def get_redmine_group(self, group_id):
        self.request_error_handler.set_next(self.group_data_handler)
        query = self._get_redmine_group_request(group_id=group_id, include="users")
        return await self.request_error_handler.validate(lambda: self.new_session_request(query))

    async def get_redmine_user_info(self, user_id, start_date, end_date):
        self.request_error_handler.set_next(self.user_data_handler)
        query = self._get_redmine_user_request(user_id=user_id, from_date=start_date, to_date=end_date)
        return await self.request_error_handler.validate(lambda: self.new_session_request(query))

    async def get_redmine_group_users_info(self, group, start_date, end_date):
        group_with_time_sheets = group
        for user in group_with_time_sheets.users:
            data = await self.get_redmine_user_info(user.id, start_date, end_date)
            user.set_time_sheets(**data)
        return group_with_time_sheets

    def _get_redmine_group_request(self, group_id, include=None):
        return "{url}/groups/{group_id}.json?{include}&key={key}".format(
            url=self.__url,
            group_id=group_id,
            include="include={include}".format(include=include) if include else "",
            key=self.__token)

    def _get_redmine_user_request(self, user_id, from_date, to_date):
        return '{url}/time_entries.json?user_id={user_id}&from={from_date}&to={to_date}&key={key}'.format(
            url=self.__url,
            user_id=user_id,
            from_date=from_date,
            to_date=from_date if to_date is None else to_date,
            key=self.__token
        )
