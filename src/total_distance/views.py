import datetime as dt
import json

from asgiref.sync import sync_to_async
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from total_distance.models import ApiRequest
from total_distance.utils import get_distance, get_data_from_request


def main(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


async def path_distance(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        start = dt.datetime.now()
        request_id, coordinates = get_data_from_request(request)
        api_request, _ = await sync_to_async(
            ApiRequest.objects.get_or_create,
            thread_sensitive=True,
        )(request_id=request_id)
        results = await get_distance(coordinates=coordinates)
        distance = sum(results)
        end = dt.datetime.now()
        api_request.calculations_start = start
        api_request.calculations_end = end
        await sync_to_async(api_request.save, thread_sensitive=True)()

        return HttpResponse(
            json.dumps(
                {
                    "distance": round(distance, 2),
                    "processing_time": api_request.duration,
                }
            )
        )
