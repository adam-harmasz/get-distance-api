import asyncio
import json
import os
import time
from typing import List, Tuple

import httpx
from asgiref.sync import sync_to_async, async_to_sync
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from total_distance.forms import RequestForm


@csrf_exempt
def path_distance(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = RequestForm()
        return render(request, "index.html", context={"form": form})

    if request.method == "POST":
        start = time.perf_counter()
        request_json = json.loads(request.body.decode())
        request_id = request_json["requestId"]
        coordinates = request_json["coordinates"]
        results = get_distance(coordinates=coordinates)
        print(sum(results))
        end = time.perf_counter()
        print(f"Time elapsed: {end - start}")
        return HttpResponse(request.POST)


@async_to_sync
async def get_distance(coordinates: List[List]) -> List[float]:
    async with httpx.AsyncClient(
        auth=httpx.BasicAuth(
            username=os.getenv("API_USERNAME"), password=os.getenv("API_PASSWORD")
        )
    ) as session:
        results = await asyncio.gather(
            *[
                geo_distance_request(session, coordinate, coordinates[idx + 1])
                for idx, coordinate in enumerate(coordinates[:-1])
            ]
        )
    return results


async def geo_distance_request(session, origin, destination):
    url = "http://64.227.65.68:3006/route"
    params = dict(
        origin=f"{origin[0]},{origin[1]}",
        destination=f"{destination[0]},{destination[1]}",
    )
    print(params)
    response = await session.get(url, params=params)
    print(dir(response))
    print(response.content)
    return float(json.loads(response.content.decode())["distance"])
