from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("core.urls.user")),
    path("api/game/", include("core.urls.game")),
    path("api/leaderboard/", include("core.urls.leaderboard")),
    path("api/admin/", include("core.urls.admin"))
]
