from django.db import models

# Create your models here.
class Hero_Section(models.Model):
    hero_text_title = models.CharField(max_length=60)
    hero_text_body = models.TextField(max_length=300)
    hero_image = models.ImageField(upload_to='main/images/')

    def __str__(self):
        return f"{self.hero_text_title} - {self.hero_text_body[:50]} ..."
    


