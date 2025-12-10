from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from core.views.leaderboard import get_leaderboard_month, get_leaderboard_week

urlpatterns = [
    path("get_leaderboard_week/", get_leaderboard_week,),
    path("get_leaderboard_month/", get_leaderboard_month,),
]
