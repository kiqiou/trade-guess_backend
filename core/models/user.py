from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

class User(AbstractUser):
    telegram_username = models.CharField(max_length=100, null=True, blank=True)
    role = models.ForeignKey('core.Role', on_delete=models.CASCADE, default=1)

    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='core_user_set',  # Изменяем default related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='core_user_permissions_set', 
        blank=True
    )

class DailyStatistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    daily_attempts = models.IntegerField(null=True)
    daily_correct_attempts = models.IntegerField(null=True)
    daily_accuracy = models.SmallIntegerField(null=True)
    streak = models.SmallIntegerField(null=True)

class UserStatistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_attempts = models.IntegerField(null=True)
    correct_attempts = models.IntegerField(null=True)
    accuracy_percent = models.SmallIntegerField(null=True)
    week_accuracy = models.SmallIntegerField(null=True)
    month_accuracy = models.SmallIntegerField(null=True)
