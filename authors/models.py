from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    short_bio = models.TextField(max_length=500)
    location = models.TextField(
        max_length=300, help_text="street, city/district, region, country")
    profession = models.CharField(
        max_length=200, help_text="Profesional Mathematical Teacher")
    employed = models.BooleanField(default=False)
    place_of_employment = models.CharField(
        null=True, blank=True, max_length=250)
    job_duration = models.PositiveSmallIntegerField(blank=True, null=True)
    seeking_job = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Sponsor(models.Model):
    renewals = [("month", "Per month"), ("yearly", "Per year")]
    sponsor_name = models.CharField(max_length=100)
    sponsor_logo = models.ImageField(upload_to="Sponsors")
    amount = models.FloatField()
    short_bio = models.TextField(max_length=400)
    sponsor_from = models.DateTimeField(auto_now=True)
    renewal = models.CharField(choices=renewals, max_length=20)

    def __str__(self):
        return self.sponsor_name
