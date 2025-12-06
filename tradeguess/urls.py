from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("core.urls.user")),
    path("api/game/", include("core.urls.game"))
]
