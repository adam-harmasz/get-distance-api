from django.db import models


class ApiRequest(models.Model):
    request_id = models.CharField(unique=True, max_length=50)
    path_coordinates = models.TextField(blank=False)
    calculations_start = models.DateTimeField()
    calculations_end = models.DateTimeField()

    def __str__(self) -> str:
        return f"Request id: {self.request_id}"

    @property
    def calculation_duration(self) -> float:
        return (self.calculations_end - self.calculations_start).seconds
