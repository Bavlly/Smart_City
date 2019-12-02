from django.db import models

# Create your models here.
class Sensors(models.Model):
    sensor_ID = models.IntegerField()
    sensorValue = models.IntegerField()