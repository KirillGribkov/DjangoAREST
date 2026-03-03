from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    temperature = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    surface_pressure = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.name
    
class WeatherUser(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class WeatherUserCity(models.Model):
    user_id =  models.ForeignKey(WeatherUser, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    temperature = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    surface_pressure = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.name

