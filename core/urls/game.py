from django.urls import path
from core.views.game import get_challenge, resolve_attempt

urlpatterns = [
    path("chart/", get_challenge),
    path("guess/<int:attempt_id>/", resolve_attempt),
]
