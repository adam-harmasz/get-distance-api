from django.contrib import admin

from total_distance.models import ApiRequest, ApiRequestResult

admin.site.register(ApiRequest)
admin.site.register(ApiRequestResult)
