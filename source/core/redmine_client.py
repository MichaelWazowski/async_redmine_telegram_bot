from source.core.http_client import HTTPClient
from source.utils.request_handler import RequestErrorHandler


class RedmineClient:
    @staticmethod
    async def new_session_request(request_body):
        new_session = HTTPClient()
        return await new_session.make_request(request_body)

    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token
        self.request_error_handler = RequestErrorHandler()

    async def get_redmine_group(self, group_id):
        request_body = self._get_redmine_group_request(group_id=group_id, include="users")
        return await self.request_error_handler.validate(lambda: self.new_session_request(request_body))

    async def get_redmine_user_info(self, user_id, start_date, end_date=None):
        request_body = self._get_redmine_user_request(user_id=user_id, from_date=start_date, to_date=end_date)
        return await self.request_error_handler.validate(lambda: request_body)

    def _get_redmine_group_request(self, group_id, include=None):
        return "{url}/groups/{group_id}.json?{include}&key={key}".format(
            url=self.url,
            group_id=group_id,
            include="include={include}".format(include=include) if include else "",
            key=self.token)

    def _get_redmine_user_request(self, user_id, from_date, to_date):
        return '{url}/time_entries.json?user_id={user_id}&from={from_date}&to={to_date}&key={key}'.format(
            url=self.url,
            user_id=user_id,
            from_date=from_date,
            to_date=from_date if to_date is None else to_date,
            key=self.token
        )
