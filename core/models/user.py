from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

class MyUser(models.Model):
    telegram_username = models.CharField(null=True,) #Пока что может быть пустым
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=1) 

class DailyStatistics(models.Model):
    user_id = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    daily_attempts = models.IntegerField(null=True)
    daily_correct_attempts = models.IntegerField(null=True)
    daily_accuracy = models.SmallIntegerField(null=True)
    streak = models.SmallIntegerField(null=True)

class UserStatistics(models.Model):
    user_id = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    total_attempts = models.IntegerField(null=True)
    correct_attempts = models.IntegerField(null=True)
    accuracy_percent = models.SmallIntegerField(null=True)
    week_accuracy = models.SmallIntegerField(null=True)
    month_accuracy = models.SmallIntegerField(null=True)
