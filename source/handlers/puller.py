import asyncio
from source.clients.redmine_client import RedmineClient
from source.handlers.request_handler import RequestErrorHandler
from source.data_classes.rm_group import RMGroup


class Puller:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        # self.queue = pull_queue
        self.rm_client = RedmineClient(url, token)
        self.request_error_handler = RequestErrorHandler()

    async def get_redmine_group(self, group_id):
        result = await self.rm_client.get_redmine_group(group_id)
        if isinstance(result, RMGroup):
            group = await self.rm_client.get_redmine_group_users_info(result, "2022-05-05")
            print(group)
        return result
