from aiohttp import web
from src.misc import add_optionally_slashed_route, validatable
from src.services.sample import SampleService

class Sample(web.Application):
    def __init__(self):
        super().__init__()
        self['sample_service'] = SampleService()
        self['default_headers'] = {'charset': 'utf-8'}
        self.add_routes([*add_optionally_slashed_route(web.get, '/{a}/plus/{b}', calculate_sum)])

    def post_init(self, parent) -> None:
        self['schemas'] = parent['schemas']


async def calculate_sum(request: web.Request):
    a = int(request.match_info['a'])
    b = int(request.match_info['b'])
    return web.json_response({
            'data': {
                'sum': request.app['sample_service'].sum(a, b)
            }
        }, headers={**request.app['default_headers']})