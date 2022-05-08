import aiohttp


class HTTPClient:

    def __init__(self):
        self.client = aiohttp.ClientSession()

    async def make_request(self, work_queue):
        responses_dict = {}
        async with self.client as session:
            while not work_queue.empty():
                query = await work_queue.get()
                async with session.get(query["url"]) as response:
                    if not response.raise_for_status():
                        responses_dict[query["id"]] = await response.json()
        return responses_dict
