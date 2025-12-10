from rest_framework import serializers

from core.models.game import Asset, Attempt, ChartSnapshot
from core.models.user import DailyStatistics, PlatformDailyActivity, User, Role, UserStatistics


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = ["id", "telegram_username", "role", "is_active"]

class DailyStatisticsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DailyStatistics
        fields = [
            "id", "user", "date",
            "daily_attempts", "daily_correct_attempts",
            "daily_accuracy", "streak"
        ]

class UserStatisticsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    accuracy = serializers.FloatField(read_only=True)

    class Meta:
        model = UserStatistics
        fields = [
            "id", "user",
            "total_attempts", "correct_attempts",
            "accuracy_percent", "week_accuracy",
            "month_accuracy", "accuracy"
        ]

class PlatformDailyActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformDailyActivity
        fields = "__all__"

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"

class ChartSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartSnapshot
        fields = ('id','asset','visible_candles','timeframe','visible_len')

class AttemptCreateSerializer(serializers.ModelSerializer):
    snapshot_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Attempt
        fields = ('id','snapshot_id','decision','success','created_at','resolved_at')

class AttemptResolveSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=(("LONG","LONG"),("SHORT","SHORT")))
