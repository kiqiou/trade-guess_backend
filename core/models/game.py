from django.db import models
from core.models.user import User

class Asset(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    ohlc_cache = models.JSONField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

class ChartSnapshot(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    visible_candles = models.JSONField()  # list of OHLC dicts
    outcome_candles = models.JSONField()  # list of OHLC dicts used to check the result
    created_at = models.DateTimeField(auto_now_add=True)
    timeframe = models.CharField(max_length=10, default="1h")
    visible_len = models.IntegerField(default=50)
    outcome_len = models.IntegerField(default=10)

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts")
    snapshot = models.ForeignKey(ChartSnapshot, on_delete=models.SET_NULL, null=True, blank=True)
    decision = models.CharField(max_length=5, null=True, choices=(("LONG","LONG"),("SHORT","SHORT")))
    success = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

