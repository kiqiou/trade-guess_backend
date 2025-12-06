from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models.game import Attempt, ChartSnapshot
from core.models.user import DailyStatistics, UserStatistics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_challenge(request):
    user = request.user
    today = timezone.localdate()

    ds, _ = DailyStatistics.objects.get_or_create(
        user=user,
        defaults={"date": today, "daily_attempts": 0, "daily_correct_attempts": 0, "daily_accuracy": 0, "streak": 0}
    )

    if ds.date != today:
        ds.date = today
        ds.daily_attempts = 0
        ds.daily_correct_attempts = 0
        ds.daily_accuracy = 0
        ds.streak = 0
        ds.save()

    if ds.daily_attempts >= 10:
        return Response({"detail": "Daily limit reached"}, status=403)

    snapshot = ChartSnapshot.objects.order_by("?").first()
    if not snapshot:
        return Response({"detail": "No snapshots available"}, status=500)

    attempt = Attempt.objects.create(user=user, snapshot=snapshot)

    return Response({
        "attempt_id": attempt.id,
        "asset": snapshot.asset.symbol,
        "visible_candles": snapshot.visible_candles,
        "remaining_attempts": 10 - ds.daily_attempts,
    })

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def resolve_attempt(request, attempt_id):
    user = request.user
    decision = request.data.get("decision")
    if decision not in ("LONG", "SHORT"):
        return Response({"detail": "decision required LONG/SHORT"}, status=400)

    attempt = get_object_or_404(Attempt, id=attempt_id, user=user)
    if attempt.resolved_at is not None:
        return Response({"detail": "already resolved"}, status=400)

    snapshot = attempt.snapshot
    if not snapshot:
        return Response({"detail": "snapshot missing"}, status=500)

    last_visible = snapshot.visible_candles[-1]["close"]
    last_outcome = snapshot.outcome_candles[-1]["close"]
    success = (last_outcome > last_visible and decision == "LONG") or \
              (last_outcome < last_visible and decision == "SHORT")

    attempt.decision = decision
    attempt.success = success
    attempt.resolved_at = timezone.now()
    attempt.save()

    # Daily stats
    ds, _ = DailyStatistics.objects.get_or_create(user=user)
    today = timezone.localdate()
    if ds.date != today:
        ds.date = today
        ds.daily_attempts = 0
        ds.daily_correct_attempts = 0
        ds.streak = 0

    ds.daily_attempts = (ds.daily_attempts or 0) + 1
    if success:
        ds.daily_correct_attempts = (ds.daily_correct_attempts or 0) + 1
        ds.streak = (ds.streak or 0) + 1
    else:
        ds.streak = 0
    ds.daily_accuracy = int(100 * (ds.daily_correct_attempts or 0) / ds.daily_attempts)
    ds.save()

    # Global stats
    us, _ = UserStatistics.objects.get_or_create(user=user)
    us.total_attempts = (us.total_attempts or 0) + 1
    if success:
        us.correct_attempts = (us.correct_attempts or 0) + 1

    total_attempts = us.total_attempts or 0
    correct_attempts = us.correct_attempts or 0
    us.accuracy_percent = int(100 * correct_attempts / total_attempts) if total_attempts > 0 else 0
    us.save()

    return Response({
        "success": success,
        "last_visible_close": last_visible,
        "last_outcome_close": last_outcome,
        "daily": {
            "attempts": ds.daily_attempts,
            "correct": ds.daily_correct_attempts,
            "accuracy": ds.daily_accuracy,
            "streak": ds.streak,
        },
        "global": {
            "total_attempts": us.total_attempts,
            "correct_attempts": us.correct_attempts,
            "accuracy_percent": us.accuracy_percent,
        }
    })