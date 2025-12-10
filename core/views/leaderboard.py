import math
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models.user import UserStatistics

def build_leaderboard(user_stats, accuracy_field):
    leaderboard = []
    for s in user_stats:
        attempts = s.total_attempts or 0
        accuracy = getattr(s, accuracy_field) or 0
        rating = accuracy * math.log(1 + attempts)

        leaderboard.append({
            "user": s.user.telegram_username,
            "attempts": attempts,
            "accuracy": accuracy,
            "rating": rating,
        })

    # сортировка по рейтингу
    leaderboard.sort(key=lambda x: x["rating"], reverse=True)
    return leaderboard

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_leaderboard_week(request):
    stats = UserStatistics.objects.select_related("user").all()
    leaderboard = build_leaderboard(stats, "week_accuracy")

    top_100 = leaderboard[:100]

    user_rank = None
    for idx, item in enumerate(leaderboard, start=1):
        if item["user"] == request.user.telegram_username:
            user_rank = idx
            break

    return Response({
        "leaderboard": top_100,
        "user_rank": user_rank
    }, status=200)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_leaderboard_month(request):
    stats = UserStatistics.objects.select_related("user").all()
    leaderboard = build_leaderboard(stats, "month_accuracy")

    top_100 = leaderboard[:100]

    user_rank = None
    for idx, item in enumerate(leaderboard, start=1):
        if item["user"] == request.user.telegram_username:
            user_rank = idx
            break

    return Response({
        "leaderboard": top_100,
        "user_rank": user_rank
    }, status=200)
