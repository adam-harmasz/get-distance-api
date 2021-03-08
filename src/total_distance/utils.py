import asyncio
import json
import os
from typing import List, Tuple

import httpx
from django.http import HttpRequest

from total_distance.validators import validate_geo_api_response, validate_coordinates


async def get_distance(coordinates: List[List[str]]) -> List[float]:
    async with httpx.AsyncClient(
        auth=httpx.BasicAuth(
            username=os.getenv("API_USERNAME"), password=os.getenv("API_PASSWORD")
        ),
        timeout=11.0,
    ) as session:
        results = await asyncio.gather(
            *[
                geo_distance_request(session, coordinate, coordinates[idx + 1])
                for idx, coordinate in enumerate(coordinates[:-1])
            ]
        )

    return results


async def geo_distance_request(
    session: httpx.AsyncClient, origin: List[float], destination: List[float]
):
    url = "http://64.227.65.68:3006/route"
    params = dict(
        origin=f"{origin[0]},{origin[1]}",
        destination=f"{destination[0]},{destination[1]}",
    )
    response = await session.get(url, params=params)
    response.raise_for_status()
    print(response)

    return validate_geo_api_response(response)


def get_data_from_request(request: HttpRequest) -> Tuple[str, List[List[str]]]:
    request_json = json.loads(request.body.decode())
    request_id = request_json["requestId"]
    coordinates = validate_coordinates(request_json["coordinates"])

    return request_id, coordinates
