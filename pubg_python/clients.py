import json

import furl
import requests

from . import exceptions


class Client:

    API_OK = 200
    API_ERRORS_MAPPING = {
        401: exceptions.UnauthorizedError,
        404: exceptions.NotFoundError,
        415: exceptions.InvalidContentTypeError,
        429: exceptions.RateLimitError,
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/vnd.api+json'})
        self.url = furl.furl()

    def request(self, endpoint):
        response = self.session.get(endpoint)

        if response.status_code != self.API_OK:
            exception = self.API_ERRORS_MAPPING.get(
                response.status_code, exceptions.APIError)
            raise exception()

        return json.loads(response.text)


class APIClient(Client):

    BASE_URL = 'https://api.playbattlegrounds.com/'

    def __init__(self, api_key):
        super().__init__()
        self.session.headers.update({'Authorization': api_key})
        self.url.set(path=self.BASE_URL)


class TelemetryClient(Client):
    pass
