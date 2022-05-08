import asyncio
from source.data_classes.rm_group import RMGroup


class MessageCreator:
    @staticmethod
    def create_message(item):
        message = str(item)
        for i, user in enumerate(item.users, start=1):
            message += f"{i}) {user}"
        return message

    def __init__(self, request_queue: asyncio.Queue, response_queue: asyncio.Queue, coworkers):
        self.request_queue = request_queue
        self.response_queue = response_queue
        self.coworkers = coworkers

    async def worker(self):
        q_item = await self.request_queue.get()
        if isinstance(q_item, RMGroup):
            message = self.create_message(q_item)
        else:
            message = q_item.message
        await self.response_queue.put(dict(chat_id=q_item.chat_id, message=message))
        self.request_queue.task_done()

    async def start(self):
        workers = [asyncio.create_task(self.worker()) for number in range(self.coworkers)]
        await asyncio.gather(*workers)
        await self.request_queue.join()
        for worker in workers:
            worker.cancel()
