from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models.user import PlatformDailyActivity, User, UserStatistics
from core.serializers import PlatformDailyActivitySerializer, UserSerializer, UserStatisticsSerializer

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_platform_stats(request):
    """
    GET /api/admin/get_platform_stats/

    Принимает:
        - ничего (только авторизацию по токену)

    Возвращает:
        - список объектов PlatformDailyActivity
    [
        {
            "id": 1,
            "date": "2025-12-10",
            "total_attempts": 2,
            "correct_attempts": 1,
            "average_accuracy": 50.0,
            "active_users": 1
        }
    ]
    """
    stats = PlatformDailyActivity.objects.order_by("-date")
    serializer = PlatformDailyActivitySerializer(stats, many=True)
    return Response(serializer.data, status=200)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_users_and_stats_list(request):
    """
    GET /api/admin/get_users_and_stats_list/

    Принимает:
        - ничего (только авторизацию по токену)

    Возвращает:
        {
    "users": [
        {
            "id": 1,
            "telegram_username": "kiqiou",
            "role": {
                "id": 1,
                "name": "client"
            },
            "is_active": true
        }
    ],
    "statistics": [
        {
            "id": 1,
            "user": {
                "id": 1,
                "telegram_username": "kiqiou",
                "role": {
                    "id": 1,
                    "name": "client"
                },
                "is_active": true
            },
            "total_attempts": 4,
            "correct_attempts": 2,
            "accuracy_percent": 50,
            "week_accuracy": 40,
            "month_accuracy": 40
        }
    ]
    }
    """
    users = User.objects.all()
    stats = UserStatistics.objects.all()

    users_serializer = UserSerializer(users, many=True)
    stats_serializer = UserStatisticsSerializer(stats, many=True)

    return Response({
        "users": users_serializer.data,
        "statistics": stats_serializer.data
    }, status=200)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ban_user(request, user_id):
    """
    POST /api/admin/ban/<user_id>/

    Принимает:
        - user_id (в URL) 
        (авторизацию по токену)

    Возвращает:
        {"detail": "User <username> banned"}

    Действие:
        - помечает пользователя как неактивного (user.is_active = False)
    """
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return Response({"detail": f"User {user.username} banned"}, status=200)
