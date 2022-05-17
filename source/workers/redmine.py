import asyncio
from source.clients.redmine_client import RedmineClient
from source.handlers.request_handler import GroupDataHandler
from source.data_classes.rm_group import RMGroup
from source.data_classes.errors import RequestError


class Redmine:
    def __init__(self, request_queue: asyncio.Queue):
        self.request_queue = request_queue
        self.rm_client = RedmineClient()
        self.group_data_handler = GroupDataHandler()

    async def set_redmine_group_time_sheets(self, group: RMGroup, start_date: str, end_date: str):
        group_with_time_sheets = group
        for user in group_with_time_sheets.users:
            user_data = await self.rm_client.get_redmine_user_data(user.id, start_date, end_date)
            user.set_time_sheets(user_data)
        return group_with_time_sheets

    async def worker(self, group_id: int, chat_id: str, start_date: str, end_date: str, filtered_status: bool):
        try:
            group = await self.rm_client.get_redmine_group(group_id)
            group.filtered = filtered_status
            result = await self.set_redmine_group_time_sheets(group, start_date, end_date)
        except RequestError as error:
            result = error
        result.chat_id = chat_id
        await self.request_queue.put(result)
