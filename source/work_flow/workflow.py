import asyncio
import time
from source.workers.redmine import Redmine
from source.workers.sender import Sender
from source.data_classes.data_package import DataPackage
from telegram.ext import CallbackContext


class WorkFlow:
    def __init__(self):
        self.request_queue = asyncio.Queue()
        self.poller = Redmine(self.request_queue)
        self.sender = Sender(self.request_queue)
        self.loop = asyncio.get_event_loop()

    async def _create_workflow(self, group_id, chat_id, from_date, to_date, filter_status):
        await self.poller.worker(group_id, chat_id, from_date, to_date, filter_status)
        await self.sender.start()

    async def gather_task(self, data: DataPackage):
        tasks = [asyncio.create_task(self._create_workflow(
            group_id,
            data.chat_id,
            data.from_date,
            data.to_date,
            data.filter_status))
            for group_id in data.ids_list]
        await asyncio.gather(*tasks)

    def set_task(self, data: DataPackage or CallbackContext):
        if isinstance(data, CallbackContext):
            data = data.job.context
        task = self.loop.create_task(self.gather_task(data))
        while self.loop.is_running():
            time.sleep(0.1)
        self.loop.run_until_complete(task)
