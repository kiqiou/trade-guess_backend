from rest_framework import serializers

from core.models.game import Asset, Attempt, ChartSnapshot
from core.models.user import DailyStatistics, MyUser, Role, UserStatistics


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = MyUser
        fields = ["id", "telegram_username", "role", ]

class DailyStatisticsSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="user_id", read_only=True)

    class Meta:
        model = DailyStatistics
        fields = [
            "id", "user_id", "user", "date",
            "daily_attempts", "daily_correct_attempts",
            "daily_accuracy", "streak"
        ]

class UserStatisticsSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="user_id", read_only=True)
    accuracy = serializers.FloatField(read_only=True)

    class Meta:
        model = UserStatistics
        fields = [
            "id", "user_id", "user",
            "total_attempts", "correct_attempts",
            "accuracy_percent", "week_accuracy",
            "month_accuracy", "accuracy"
        ]

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"

class AttemptSerializer(serializers.ModelSerializer):
    user = UserSerializer(source="user_id", read_only=True)
    asset_data = AssetSerializer(source="asset", read_only=True)

    class Meta:
        model = Attempt
        fields = [
            "id", "user_id", "user",
            "asset", "asset_data",
            "success", "created_at", "resolved_at"
        ]

class ChartSnapshotSerializer(serializers.ModelSerializer):
    asset_data = AssetSerializer(source="asset", read_only=True)

    class Meta:
        model = ChartSnapshot
        fields = [
            "id", "asset", "asset_data",
            "visible_candles", "outcome_candles",
            "created_at"
        ]
