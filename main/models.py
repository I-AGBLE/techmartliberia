from django.db import models

# Create your models here.
class Hero_Section(models.Model):
    hero_text_title = models.CharField(max_length=100)
    hero_text_body = models.TextField()
    hero_image = models.ImageField(upload_to='main/images/')

    def __str__(self):
        return self.hero_text_title
    


