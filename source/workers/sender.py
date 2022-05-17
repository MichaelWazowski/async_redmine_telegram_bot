import os
import asyncio
from source.clients.telegram_client import TelegramClient


class Sender:
    def __init__(self, response_queue: asyncio.Queue):
        self.tg_client = TelegramClient(os.getenv("TELEGRAM_TOKEN"))
        self.response_queue = response_queue

    async def sender(self):
        q_item = await self.response_queue.get()
        self.tg_client.send_message(q_item.chat_id, str(q_item))
        self.response_queue.task_done()

    async def start(self):
        await asyncio.gather(asyncio.create_task(self.sender()))
        await self.response_queue.join()
