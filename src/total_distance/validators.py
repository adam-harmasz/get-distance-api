from typing import List

from django.core.exceptions import ValidationError


def validate_coordinates(coordinates: List[List[str]]) -> List[List[str]]:
    for coordinate in coordinates:
        validate_coordinate_points(coordinate)
        validate_coordinate_type(coordinate)
    return coordinates


def validate_coordinate_type(coordinate: List[str]) -> None:
    try:
        float(coordinate[0])
        float(coordinate[1])
    except ValueError:
        raise ValidationError("Improper type of coordinate")


def validate_coordinate_points(coordinate: List[str]) -> None:
    if len(coordinate) != 2:
        raise ValidationError("Coordinate must contain longitude and latitude")


def validate_request_id(request_id: str) -> str:
    if not isinstance(request_id, str) or not request_id:
        raise ValidationError("Improper type of request id")

    return request_id