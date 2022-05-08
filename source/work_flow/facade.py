import asyncio
from source.workers.puller import Puller
from source.workers.message_creator import MessageCreator
from source.workers.sender import Sender


class Facade:
    def __init__(self, url: str, token: str, ids_list: list):
        self.request_queue = asyncio.Queue()
        self.response_queue = asyncio.Queue()
        self.ids_list = ids_list
        self.puller = Puller(url, token, self.request_queue)
        self.message_creator = MessageCreator(self.request_queue, self.response_queue, len(self.ids_list))
        self.sender = Sender(self.response_queue, len(self.ids_list))

    async def create_workflow(self, group_id, chat_id):
        await self.puller.worker(group_id, "2022-05-05", None)
        await self.message_creator.start()
        await self.sender.start(chat_id)

    async def get_all_time_sheets(self, chat_id):
        tasks = [asyncio.create_task(self.create_workflow(group_id, chat_id)) for group_id in self.ids_list]
        await asyncio.gather(*tasks)

    def start(self, chat_id):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.get_all_time_sheets(chat_id))
        loop.run_until_complete(task)


def main():
    bot = Facade('http://redmine.cml2.local', '0e129cd8e85e726677feec971d4471899a8f73f8', [312, 311])
    bot.start("-639533828")


if __name__ == '__main__':
    main()
