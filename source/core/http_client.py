import aiohttp


class HTTPClient:

    @staticmethod
    def request_error_handler(input_request):
        async def error_wrapped_request(*args, **kwargs):
            try:
                response = await input_request(*args, **kwargs)
                return response
            except aiohttp.ClientConnectorError as connector_error:
                return ConnectionError(f"Connection failed: {str(connector_error.host)}")
            except aiohttp.ClientResponseError as response_error:
                return ValueError(
                    f"Resource {str(response_error.message).lower()} "
                    f"in host {str(response_error.request_info.url.raw_host)}")

        return error_wrapped_request

    def __init__(self):
        self.client = aiohttp.ClientSession()

    async def make_request(self, request):
        async with self.client as session:
            async with session.get(request) as response:
                if not response.raise_for_status():
                    json = await response.json()
                    return json
