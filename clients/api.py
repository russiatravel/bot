import os

import httpx
from pydantic import BaseModel


class City(BaseModel):
    uid: int
    name: str
    description: str


class CityClient:
    def __init__(self, url: str) -> None:
        self.url = f'{url}/cities'

    def get_all(self) -> list[City]:
        response = httpx.get(url=f'{self.url}/')
        response.raise_for_status()
        cities = response.json()

        return [City(**city) for city in cities]


class PlaceClient:
    def __init__(self, url: str) -> None:
        self.url = f'{url}/places'


class ApiClient:
    def __init__(self, url: str) -> None:
        self.url = url
        self.cities = CityClient(url)
        self.places = PlaceClient(url)


client = ApiClient(os.environ['API_URL'])
