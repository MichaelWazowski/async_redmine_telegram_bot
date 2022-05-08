import asyncio
import os
from source.clients.telegram_client import TelegramClient


class Sender:
    def __init__(self, response_queue: asyncio.Queue, co_senders):
        self.tg_client = TelegramClient('1959693479:AAEycqFwzSQTgeJhJL9-d9mD4AiE1hKl5pQ')
        self.co_senders = co_senders
        self.response_queue = response_queue

    async def sender(self, chat_id):
        q_item = await self.response_queue.get()
        self.tg_client.send_message(chat_id, q_item)
        self.response_queue.task_done()

    async def start(self, chat_id):
        senders = [asyncio.create_task(self.sender(chat_id)) for number in range(self.co_senders)]
        await asyncio.gather(*senders)
        await self.response_queue.join()
        for sender in senders:
            sender.cancel()
