from typing import Optional

from django.db import models


class ApiRequest(models.Model):
    request_id = models.CharField(unique=True, max_length=50)
    calculations_start = models.DateTimeField(null=True)
    calculations_end = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"Request id: {self.request_id}"

    @property
    def duration(self) -> Optional[float]:
        if self.calculations_start and self.calculations_end:
            return round(
                self.calculations_end.timestamp() - self.calculations_start.timestamp(),
                2,
            )
        return None

    @property
    def is_finished(self):
        return "Finished" if self.calculations_end else "In progress"
