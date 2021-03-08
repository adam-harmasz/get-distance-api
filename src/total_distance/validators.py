import json
from json.decoder import JSONDecodeError
from typing import List

import httpx
from django.core.exceptions import ValidationError


def validate_coordinates(coordinates: List[List[str]]) -> List[List[str]]:
    if len(coordinates) >= 2:
        for coordinate in coordinates:
            validate_coordinate_points(coordinate)
            validate_coordinate_type(coordinate)
        return coordinates
    raise ValidationError(
        "There need to be more than two coordinates to calculate path"
    )


def validate_coordinate_type(coordinate: List[str]) -> None:
    try:
        latitude = float(coordinate[0])
        longitude = float(coordinate[1])
    except ValueError:
        raise ValidationError("Improper type of coordinate")


def validate_latitude_range(latitude: float) -> float:
    if -90 > latitude > 90:
        return latitude
    raise ValidationError("Latitude needs to be in range -90, 90")


def validate_longitude_range(longitude: float) -> float:
    if -180 > longitude > 180:
        return longitude
    raise ValidationError("Longitude needs to be in range -180, 180")

def validate_coordinate_points(coordinate: List[str]) -> None:
    if len(coordinate) != 2:
        raise ValidationError("Coordinate must contain longitude and latitude")


def validate_request_id(request_id: str) -> str:
    if not isinstance(request_id, str) or not request_id:
        raise ValidationError("Improper type of request id")

    return request_id


def validate_geo_api_response(response: httpx.Response) -> float:
    try:
        return float(json.loads(response.content.decode())["distance"])
    except (ValueError, JSONDecodeError):
        raise ValidationError("Unexpected response from eternal API")
