from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from core.models.user import DailyStatistics, User, Role, UserStatistics
from core.serializers import DailyStatisticsSerializer, UserSerializer, UserStatisticsSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def username_auth(request):
    """
    GET /api/user/auth/

    Принимает:
        - юзернейм
        {
            "username": "kiqiou"
        }


    Возвращает:
    {
        "created": false, // если пользователь уже зарегистрирован, то фолз, если создан, то тру
        "user": {
            "id": 1,
            "telegram_username": "kiqiou",
            "role": {
                "id": 1,
                "name": "client"
            },
            "is_active": false // или True если не забанен
        },
        "statistics": {
            "id": 1,
            "user": {
                "id": 1,
                "telegram_username": "kiqiou",
                "role": {
                    "id": 1,
                    "name": "client"
                },
                "is_active": false
            },
            "total_attempts": 4,
            "correct_attempts": 2,
            "accuracy_percent": 50,
            "week_accuracy": 40,
            "month_accuracy": 40
        },
        "daily_statistics": {
            "id": 1,
            "user": {
                "id": 1,
                "telegram_username": "kiqiou",
                "role": {
                    "id": 1,
                    "name": "client"
                },
                "is_active": false
            },
            "date": "2025-12-10",
            "daily_attempts": 2,
            "daily_correct_attempts": 1,
            "daily_accuracy": 50,
            "streak": 1
        },
        "token": "6e237cf5ea23ec49a923023109bca475a07cde0c"
    }
    """
    username = request.data.get("username")

    if not username:
        return Response({"detail": "username required"}, status=400)
    
    role = Role.objects.get(name="client")

    user, created = User.objects.get_or_create(
        telegram_username=username,
        defaults={"role": role}
    )

    if created:
        token = Token.objects.create(user=user)
    else:
        token = Token.objects.get(user=user)

    user_stat, _ = UserStatistics.objects.get_or_create(user=user)
    daily_user_stat, _ = DailyStatistics.objects.get_or_create(user=user)

    return Response({
        "created": created,
        "user": UserSerializer(user).data,
        "statistics": UserStatisticsSerializer(user_stat).data,
        "daily_statistics": DailyStatisticsSerializer(daily_user_stat).data,
        "token": token.key,
    }, status=200)
