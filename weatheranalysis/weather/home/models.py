from django.db import models

# Create your models here.
class TemperatureRecord(models.Model):
    city = models.CharField(max_length=255)
    temperature = models.FloatField()
    timestamp = models.DateTimeField()
