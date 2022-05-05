import aiohttp


class HTTPClient:

    def __init__(self):
        self.client = aiohttp.ClientSession()

    async def make_request(self, request):
        async with self.client as session:
            async with session.get(request) as response:
                if not response.raise_for_status():
                    json = await response.json()
                    return json
