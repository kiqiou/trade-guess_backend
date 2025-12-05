from django.db import models
from core.models.user import MyUser

class Asset(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    ohlc_cache = models.JSONField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

class Attempt(models.Model):
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="attempts")
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True)
    success = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

class ChartSnapshot(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    visible_candles = models.JSONField()
    outcome_candles = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
