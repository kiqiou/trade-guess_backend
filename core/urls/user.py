from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from core.views.user import username_auth

urlpatterns = [
    path("auth/", username_auth,),  # POST
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
]
