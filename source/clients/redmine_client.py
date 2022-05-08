import asyncio
from source.clients.http_client import HTTPClient
from source.handlers.request_handler import RequestErrorHandler, GroupDataHandler, UserDataHandler


class RedmineClient:

    @staticmethod
    async def new_session_request(work_queue):
        new_session = HTTPClient()
        # tasks = [new_session.make_request(work_queue) for task in
        #          range(work_queue.qsize() if work_queue.qsize() < 2 else 2)]
        tasks = [new_session.make_request(work_queue)]
        return await asyncio.gather(*tasks)

    def __init__(self, url: str, token: str):
        self.__url = url
        self.__token = token
        self.request_error_handler = RequestErrorHandler()
        self.group_data_handler = GroupDataHandler()
        self.user_data_handler = UserDataHandler()

    async def get_redmine_group(self, group_id):
        work_queue = asyncio.Queue()
        self.request_error_handler.set_next(self.group_data_handler)
        query = self._get_redmine_group_query(group_id=group_id, include="users")
        await work_queue.put(dict(url=query, id=group_id))
        return await self.request_error_handler.validate(lambda: self.new_session_request(work_queue))

    async def get_redmine_user(self, user_id, start_date, end_date):
        query = self._get_redmine_user_query(user_id=user_id, from_date=start_date, to_date=end_date)
        result = await self.new_session_request(query)
        return self.user_data_handler.validate(result)

    async def get_redmine_group_users_info(self, group, start_date, end_date):
        work_queue = asyncio.Queue()
        self.request_error_handler.set_next(None)
        group_with_time_sheets = group
        for user in group_with_time_sheets.users:
            await work_queue.put(
                dict(url=self._get_redmine_user_query(user_id=user.id, from_date=start_date, to_date=end_date),
                     id=user.id))
        data = await self.request_error_handler.validate(lambda: self.new_session_request(work_queue))
        return data

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
