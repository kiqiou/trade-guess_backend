from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from core.models.game import Attempt
from core.models.user import UserStatistics

@shared_task
def recalculate_stats():
    today = timezone.localdate()
    week_start = today - timedelta(days=7)
    month_start = today - timedelta(days=30)

    for stats in UserStatistics.objects.select_related("user").all():
        week_attempts = Attempt.objects.filter(user=stats.user, resolved_at__date__gte=week_start).count()
        week_correct = Attempt.objects.filter(user=stats.user, resolved_at__date__gte=week_start, success=True).count()
        stats.week_accuracy = int(100 * week_correct / week_attempts) if week_attempts > 0 else 0

        month_attempts = Attempt.objects.filter(user=stats.user, resolved_at__date__gte=month_start).count()
        month_correct = Attempt.objects.filter(user=stats.user, resolved_at__date__gte=month_start, success=True).count()
        stats.month_accuracy = int(100 * month_correct / month_attempts) if month_attempts > 0 else 0

        stats.save()
