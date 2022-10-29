import os

import httpx
from pydantic import BaseModel


class City(BaseModel):
    uid: int
    name: str
    description: str


class Place(BaseModel):
    uid: int
    name: str
    description: str
    city_id: int
    preview_image_url: str


class CityClient:
    def __init__(self, url: str) -> None:
        self.url = f'{url}/cities'

    def get_all(self) -> list[City]:
        response = httpx.get(url=f'{self.url}/')
        response.raise_for_status()
        cities = response.json()

        return [City(**city) for city in cities]

    def get_for_city(self, uid: int) -> list[Place]:
        response = httpx.get(url=f'{self.url}/{uid}/places/')
        response.raise_for_status()
        places = response.json()

        return [Place(**place) for place in places]


class PlaceClient:
    def __init__(self, url: str) -> None:
        self.url = f'{url}/places'

    def get_place(self, name: str) -> Place:
        response = httpx.get(url=f'{self.url}/?name={name}')
        response.raise_for_status()
        place = response.json()

        return Place(**place)


class ApiClient:
    def __init__(self, url: str) -> None:
        self.url = url
        self.cities = CityClient(url)
        self.places = PlaceClient(url)


client = ApiClient(os.environ['API_URL'])
