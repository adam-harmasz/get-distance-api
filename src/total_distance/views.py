import asyncio
import json
import os
import time
from typing import List, Tuple

import httpx
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from total_distance.validators import validate_coordinates


def main(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


async def path_distance(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        start = time.perf_counter()
        request_id, coordinates = get_data_from_request(request)
        results = await get_distance(coordinates=coordinates)
        distance = sum(results)
        end = time.perf_counter()
        processing_time = end - start

        return HttpResponse(
            json.dumps({"distance": distance, "processing_time": processing_time})
        )


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
    print(response.content)

    return float(json.loads(response.content.decode())["distance"])


def get_data_from_request(request: HttpRequest) -> Tuple[str, List[List[str]]]:
    request_json = json.loads(request.body.decode())
    request_id = request_json["requestId"]
    coordinates = validate_coordinates(request_json["coordinates"])

    return request_id, coordinates
