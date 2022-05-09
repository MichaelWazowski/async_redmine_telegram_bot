import asyncio
from source.clients.redmine_client import RedmineClient
from source.handlers.request_handler import RequestErrorHandler
from source.data_classes.rm_group import RMGroup


class Puller:
    def __init__(self, pull_queue: asyncio.Queue):
        self.queue = pull_queue
        self.rm_client = RedmineClient()
        self.request_error_handler = RequestErrorHandler()

    async def get_redmine_group_users_info(self, group, start_date, end_date):
        group_with_time_sheets = group
        for user in group_with_time_sheets.users:
            data = await self.rm_client.get_redmine_user(user.id, start_date, end_date)
            user.set_time_sheets(data)
        return group_with_time_sheets

    async def worker(self, group_id, chat_id, start_date, end_date):
        group = await self.rm_client.get_redmine_group(group_id)
        group.chat_id = chat_id
        if isinstance(group, RMGroup):
            group = await self.get_redmine_group_users_info(group, start_date, end_date)
        await self.queue.put(group)
