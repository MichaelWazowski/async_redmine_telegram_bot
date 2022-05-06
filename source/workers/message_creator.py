import asyncio
from source.data_classes.rm_group import RMGroup


class MessageCreator:
    def __init__(self, request_queue, coworkers):
        self.request_queue = request_queue
        self.coworkers = coworkers

    async def create_message(self):
        q_item = self.request_queue
        if isinstance(q_item, RMGroup):
            message = str(q_item)
            for i, user in enumerate(q_item.users, start=1):
                message += f"{i}) {user}"
        else:
            message = q_item
        return message

    async def start(self):
        workers = [asyncio.create_task(self.create_message()) for number in range(self.coworkers)]
        await asyncio.gather(*workers)
        await self.request_queue.join()
        for worker in workers:
            worker.cancel()
