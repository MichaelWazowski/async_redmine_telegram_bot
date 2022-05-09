import asyncio
from source.workers.puller import Puller
from source.workers.message_creator import MessageCreator
from source.workers.sender import Sender
from source.configs import init_environment


class Facade:
    def __init__(self, ids_list: list):
        init_environment()
        self.request_queue = asyncio.Queue()
        self.response_queue = asyncio.Queue()
        self.ids_list = ids_list
        self.puller = Puller(self.request_queue)
        self.message_creator = MessageCreator(self.request_queue, self.response_queue, len(self.ids_list))
        self.sender = Sender(self.response_queue, len(self.ids_list))

    async def _create_workflow(self, group_id, chat_id, from_date, to_date):
        await self.puller.worker(group_id, chat_id, from_date, to_date)
        await self.message_creator.start()
        await self.sender.start()

    async def get_time_sheets(self, chat_id, from_date, to_date):
        tasks = [asyncio.create_task(self._create_workflow(group_id, chat_id, from_date, to_date))
                 for group_id in self.ids_list]
        await asyncio.gather(*tasks)

    def set_task(self, chat_id, from_date, to_date):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.get_time_sheets(chat_id, from_date, to_date))
        loop.run_until_complete(task)


def main():
    bot = Facade([311, 312, 313, 314])
    bot.set_task("-639533828", "2022-05-05", None)


if __name__ == '__main__':
    main()
