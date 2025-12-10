from django.urls import path
from core.views.admin import ban_user, get_platform_stats, get_users_and_stats_list

urlpatterns = [
    path("get_platform_stats/", get_platform_stats),
    path("get_users_and_stats_list/", get_users_and_stats_list),
    path("ban/<int:user_id>/", ban_user),
]
