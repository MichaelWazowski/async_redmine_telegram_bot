import asyncio
from source.clients.redmine_client import RedmineClient
from source.handlers.request_handler import RequestErrorHandler
from source.data_classes.rm_group import RMGroup


class Puller:
    def __init__(self, url, token, pull_queue: asyncio.Queue):
        self.url = url
        self.token = token
        self.queue = pull_queue
        self.rm_client = RedmineClient(url, token)
        self.request_error_handler = RequestErrorHandler()

    async def get_redmine_group(self, group_id):
        result = await self.rm_client.get_redmine_group(group_id)
        return result

    async def get_user_info(self, group, start_date, end_date):
        result = await self.rm_client.get_redmine_group_users_info(group, start_date, end_date)
        return result

    async def worker(self, group_id, start_date, end_date):
        result = await self.rm_client.get_redmine_group(group_id)
        if isinstance(result, RMGroup):
            result = await self.rm_client.get_redmine_group_users_info(result, start_date, end_date)
        await self.queue.put(result)
