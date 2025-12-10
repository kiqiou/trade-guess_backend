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
    stats = PlatformDailyActivity.objects.order_by("-date")
    serializer = PlatformDailyActivitySerializer(stats, many=True)
    return Response(serializer.data, status=200)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_users_and_stats_list(request):
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
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return Response({"detail": f"User {user.username} banned"}, status=200)
