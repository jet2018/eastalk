import time
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.utils.text import slugify
from django.dispatch import receiver
from django.core.validators import validate_image_file_extension
from modules import validate_img_extension, validate_image_size

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    short_bio = models.TextField(max_length=500)
    location = models.TextField(
        max_length=300, help_text="street, city/district, region, country")
    dp = models.ImageField(upload_to="authors", blank=True, null=True, validators=[validate_image_file_extension, validate_img_extension])
    profession = models.CharField(
        max_length=200, help_text="Profesional Mathematical Teacher")
    employed = models.BooleanField(default=False)
    place_of_employment = models.CharField(
        null=True, blank=True, max_length=250)
    job_duration = models.PositiveSmallIntegerField(blank=True, null=True)
    seeking_job = models.BooleanField(default=False)
    verified_user = models.BooleanField(default=False)
    registered_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)


    def __str__(self):
        return self.user.username



class Sponsor(models.Model):
    renewals = [("none", "Not Applicable"),("month", "Per month"), ("yearly", "Per year")]
    sponsor_name = models.CharField(max_length=100)
    sponsor_logo = models.ImageField(upload_to="Sponsors")
    amount = models.FloatField()
    short_bio = models.TextField(max_length=400)
    sponsor_from = models.DateTimeField(auto_now=True)
    renewal = models.CharField(choices=renewals, max_length=20)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.sponsor_name


# signals
@ receiver(pre_save, sender=Sponsor)
def pre_save_sponsor_receiver(sender, instance, *args, **kwargs):
    instance.slug = slugify(str(time.time()))

# signals


@ receiver(pre_save, sender=Author)
def pre_save_author_receiver(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.user.first_name +"-"+instance.user.last_name+'-'+str(time.time()))
