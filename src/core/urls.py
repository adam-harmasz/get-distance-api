from django.contrib import admin
from django.urls import path

from total_distance.views import path_distance

urlpatterns = [
    path('admin/', admin.site.urls),
    path("total-distance/", path_distance),
]
