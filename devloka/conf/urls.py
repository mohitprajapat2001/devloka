from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("user.api.urls")),
    path("api/v1/", include("codespace.api.urls")),
]
