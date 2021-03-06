from django.db import models


class ApiRequest(models.Model):
    request_id = models.CharField(unique=True)

    def __str__(self) -> str:
        return f"Request id: {self.request_id}"

class ApiRequestResult(models.Model):
    api_request = models.ForeignKey(ApiRequest, related_name="api", on_delete=models.CASCADE)
    calculations_start = models.DateTimeField()