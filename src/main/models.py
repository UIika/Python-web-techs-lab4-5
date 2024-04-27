from django.db import models

class Weekday(models.TextChoices):
    MONDAY = 'Monday', 'Monday'
    TUESDAY = 'Tuesday', 'Tuesday'
    WEDNESDAY = 'Wednesday', 'Wednesday'
    THURSDAY = 'Thursday', 'Thursday'
    FRIDAY = 'Friday', 'Friday'
    SATURDAY = 'Saturday', 'Saturday'
    SUNDAY = 'Sunday', 'Sunday'

class Channel(models.Model):
    title = models.CharField(max_length=100)

class Program(models.Model):
    title = models.CharField(max_length=100)
    start_time = models.TimeField()
    weekday = models.CharField(max_length=10, choices=Weekday.choices)
    channel = models.ForeignKey(Channel, related_name='programs', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['start_time']