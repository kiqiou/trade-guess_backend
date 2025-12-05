from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from core.models.user import DailyStatistics, MyUser, Role, UserStatistics
from core.serializers import DailyStatisticsSerializer, UserSerializer, UserStatisticsSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def username_auth(request):
    username = request.data.get("username")

    if not username:
        return Response({"detail": "username required"}, status=400)
    
    role = Role.objects.get(name="client")

    user, created = MyUser.objects.get_or_create(
        telegram_username=username,
        defaults={"role": role}
    )

    user_stat, _ = UserStatistics.objects.get_or_create(user_id=user)
    daily_user_stat, _ = DailyStatistics.objects.get_or_create(user_id=user)

    return Response({
        "created": created,
        "user": UserSerializer(user).data,
        "statistics": UserStatisticsSerializer(user_stat).data,
        "daily_statistics": DailyStatisticsSerializer(daily_user_stat).data,
    }, status=200)
