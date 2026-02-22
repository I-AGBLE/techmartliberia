from django.db import models
import os
from datetime import datetime

# Create your models here.

def image_upload_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Create a timestamp string with microseconds for uniqueness
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    # Create new filename with timestamp
    new_filename = f"{timestamp}_{filename}"
    # Return the path
    return os.path.join('images', new_filename)
class Hero_Section(models.Model):
    hero_text_title = models.CharField(max_length=60)
    hero_text_body = models.TextField(max_length=300)
    hero_image = models.ImageField(upload_to=image_upload_path)

    def __str__(self):
        return f"{self.hero_text_title} - {self.hero_text_body[:50]} ..."


class Service(models.Model):
    service_title = models.CharField(max_length=60)
    service_description = models.TextField(max_length=4000)
    service_image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    service_icon = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

    def __str__(self):
        return f"{self.service_title} - {self.service_description[:50]} ..."


class Team_Member(models.Model):
    name = models.CharField(max_length=60)
    position = models.CharField(max_length=60)
    image = models.ImageField(upload_to=image_upload_path)
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.position}"



