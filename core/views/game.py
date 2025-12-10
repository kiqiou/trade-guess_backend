from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import F
from core.models.game import Attempt, ChartSnapshot
from core.models.user import DailyStatistics, PlatformDailyActivity, UserStatistics
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
    }, status=200)

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

    us, _ = UserStatistics.objects.get_or_create(user=user)
    us.total_attempts = (us.total_attempts or 0) + 1
    if success:
        us.correct_attempts = (us.correct_attempts or 0) + 1

    total_attempts = us.total_attempts or 0
    correct_attempts = us.correct_attempts or 0
    us.accuracy_percent = int(100 * correct_attempts / total_attempts) if total_attempts > 0 else 0
    
    today = timezone.localdate()
    week_start = today - timedelta(days=7)
    month_start = today - timedelta(days=30)

    week_attempts = Attempt.objects.filter(user=user, resolved_at__date__gte=week_start).count()
    week_correct = Attempt.objects.filter(user=user, resolved_at__date__gte=week_start, success=True).count()
    us.week_accuracy = int(100 * week_correct / week_attempts) if week_attempts > 0 else 0

    month_attempts = Attempt.objects.filter(user=user, resolved_at__date__gte=month_start).count()
    month_correct = Attempt.objects.filter(user=user, resolved_at__date__gte=month_start, success=True).count()
    us.month_accuracy = int(100 * month_correct / month_attempts) if month_attempts > 0 else 0

    us.save()

    pda, _ = PlatformDailyActivity.objects.get_or_create(date=today)

    pda.total_attempts = F("total_attempts") + 1
    if success:
        pda.correct_attempts = F("correct_attempts") + 1
    pda.save(update_fields=["total_attempts", "correct_attempts"])
    pda.refresh_from_db()

    has_attempt_today = Attempt.objects.filter(
        user=user, resolved_at__date=today
    ).exclude(id=attempt.id).exists()

    if not has_attempt_today:
        pda.active_users = F("active_users") + 1
        pda.save(update_fields=["active_users"])
        pda.refresh_from_db()

    if pda.total_attempts > 0:
        pda.average_accuracy = 100 * pda.correct_attempts / pda.total_attempts
        pda.save(update_fields=["average_accuracy"])

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
    },status=200)