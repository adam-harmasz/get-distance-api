import asyncio
import os

import httpx
from asgiref.sync import sync_to_async, async_to_sync
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def path_distance(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "index.html")

    if request.method == "POST":
        request_id = request.POST["request_id"]
        points = request.POST["points"]
        get_distance()
        return HttpResponse(f"{request.POST['request_id']}, {request.POST['points']}")


def get_coordinates(points: str):
    return (
        dict(longitude=float(longitude), latitude=float(latitude))
        for longitude, latitude in points.split(",")
    )


@async_to_sync
async def get_distance():
    coordinates = (
        (50.0, 18.1),
        (51.0, 19.1),
        (50.5, 15.1),
        (40.0, 18.1),
        (49.0, 16.1),
        (52.0, 18.1),
    )

    async with httpx.AsyncClient(
        auth=httpx.BasicAuth(username=os.getenv("API_USERNAME"), password=os.getenv("API_PASSWORD"))
    ) as session:  # use httpx
        await asyncio.gather(
            *[
                geo_distance_request(session, coordinate, coordinates[idx + 1])
                for idx, coordinate in enumerate(coordinates[:-1])
            ]
        )


async def geo_distance_request(session, origin, destination):
    url = "http://64.227.65.68:3006/route"
    params = dict(
        origin=f"{origin[0]},{origin[1]}",
        destination=f"{destination[0]},{destination[1]}",
    )
    print(params)
    response = await session.get(url, params=params)
    print(response)
