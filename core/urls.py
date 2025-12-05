from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from core.views.user import username_auth

urlpatterns = [
    path("auth/", username_auth,),  # POST
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
]


    # path("auth/token/", obtain_auth_token, name="api_token_auth"),
    # path("chart/", get_random_chart, name="get_chart"),  # GET
    # path("guess/", guess_direction, name="post_guess"),  # POST
    # path("me/stats/", my_stats, name="my_stats"),  # GET
    # path("leaderboard/", leaderboard, name="leaderboard"),  # GET