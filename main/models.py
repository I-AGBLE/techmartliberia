from django.db import models

# Create your models here.
class Hero_Section(models.Model):
    hero_text_title = models.CharField(max_length=60)
    hero_text_body = models.TextField(max_length=300)
    hero_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.hero_text_title} - {self.hero_text_body[:50]} ..."


class Service(models.Model):
    service_title = models.CharField(max_length=60)
    service_description = models.TextField(max_length=4000)

    def __str__(self):
        return f"{self.service_title} - {self.service_description[:50]} ..."


class Team_Member(models.Model):
    name = models.CharField(max_length=60)
    position = models.CharField(max_length=60)
    image = models.ImageField(upload_to='images/')
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.position}"



