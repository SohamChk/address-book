import aiohttp
import json

from backend.config import get_settings
from backend.log import log

async def get_coordinates(addr):

    api_key = get_settings().GEOLOC_API_KEY
    url = f'https://www.mapquestapi.com/geocoding/v1/address?key={api_key}&location={addr}'
    print(url)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:

            if str(response.status).startswith('20'):
                data = json.loads(await response.text())
                return data['results'][0]['locations'][0]['displayLatLng']
            else:
                log.error(f'Failed with status code={response.status}')