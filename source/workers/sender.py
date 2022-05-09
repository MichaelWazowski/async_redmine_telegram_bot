import os
import asyncio
from source.clients.telegram_client import TelegramClient


class Sender:
    def __init__(self, response_queue: asyncio.Queue, co_senders):
        self.tg_client = TelegramClient(os.getenv("TELEGRAM_TOKEN"))
        self.co_senders = co_senders
        self.response_queue = response_queue

    async def sender(self):
        q_item = await self.response_queue.get()
        self.tg_client.send_message(**q_item)
        self.response_queue.task_done()

    async def start(self):
        senders = [asyncio.create_task(self.sender()) for number in range(self.co_senders)]
        await asyncio.gather(*senders)
        await self.response_queue.join()
        for sender in senders:
            sender.cancel()
