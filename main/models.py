from django.db import models
import os
from datetime import datetime

from django.core.exceptions import ValidationError





# Definition of unique file names
def image_upload_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Create a timestamp string with microseconds for uniqueness
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    # Create new filename with timestamp
    new_filename = f"{timestamp}_{filename}"
    # Return the path
    return os.path.join('images', new_filename)







# -------------------------------  Home Page Hero Secion Model ---------------------------------- #
def image_upload_path(instance, filename):
    # Your existing function
    return f"heroes/{filename}"

class Hero_Section(models.Model):
    hero_text_title = models.CharField(max_length=110)
    hero_text_body = models.TextField(max_length=650)
    hero_image = models.ImageField(upload_to=image_upload_path)
    mandatory_field = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.hero_text_title} - {self.hero_text_body[:50]} ..."

    def clean(self):
        super().clean()  # First run default validations

        if self.hero_image:
            valid_extensions = ['jpeg', 'jpg', 'png']
            extension = self.hero_image.name.split('.')[-1].lower()

            if extension not in valid_extensions:
                raise ValidationError({
                    'hero_image': "Unsupported image format. Please upload JPEG, JPG, or PNG."
                })







# -------------------------------  About Page Hero Secion Model ---------------------------------- #
def image_upload_path(instance, filename):
    # Example upload path
    return f"about_heroes/{filename}"

class About_Us_Hero(models.Model):
    about_hero_text_title = models.CharField(max_length=110)
    about_hero_text_body = models.TextField(max_length=650)
    about_hero_image = models.ImageField(upload_to=image_upload_path)
    mandatory_field = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.about_hero_text_title} - {self.about_hero_text_body[:50]} ..."

    def clean(self):
        super().clean()  # Run default validations first

        # Validate about_hero_image
        if self.about_hero_image:
            valid_extensions = ['jpeg', 'jpg', 'png']
            extension = self.about_hero_image.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise ValidationError({
                    'about_hero_image': "Unsupported image format. Please upload JPEG, JPG, or PNG."
                })







# -------------------------------  Services Secion Model ---------------------------------- #
def image_upload_path(instance, filename):
    # Example upload path function
    return f"services/{filename}"

class Service(models.Model):
    service_title = models.CharField(max_length=110)
    service_description = models.TextField(max_length=5000)
    service_image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    service_icon = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    mandatory_field = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.service_title} - {self.service_description[:50]} ..."

    def clean(self):
        super().clean()  # Run default validations first

        # Validate service_image
        if self.service_image:
            valid_image_extensions = ['jpeg', 'jpg', 'png']
            extension = self.service_image.name.split('.')[-1].lower()
            if extension not in valid_image_extensions:
                raise ValidationError({
                    'service_image': "Unsupported image format. Please upload JPEG, JPG, or PNG."
                })

        # Validate service_icon
        if self.service_icon:
            valid_icon_extensions = ['svg', 'png']
            extension = self.service_icon.name.split('.')[-1].lower()
            if extension not in valid_icon_extensions:
                raise ValidationError({
                    'service_icon': "Unsupported icon format. Only SVG and PNG allowed."
                })







# -------------------------------  Meet Our Team Secion Model ---------------------------------- #
def image_upload_path(instance, filename):
    # Example upload path
    return f"team_members/{filename}"

class Team_Member(models.Model):
    name = models.CharField(max_length=35)
    position = models.CharField(max_length=35)
    image = models.ImageField(upload_to=image_upload_path)
    instagram_url = models.URLField(blank=True, null=True, max_length=255)
    twitter_url = models.URLField(blank=True, null=True, max_length=255)
    linkedin_url = models.URLField(blank=True, null=True, max_length=255)
    mandatory_field = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.name} - {self.position}"

    def clean(self):
        super().clean()  # Run default validations first

        # Validate image file
        if self.image:
            valid_extensions = ['jpeg', 'jpg', 'png']
            extension = self.image.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise ValidationError({
                    'image': "Unsupported image format. Please upload JPEG, JPG, or PNG."
                })








# -------------------------------  Why Us Secion Model ---------------------------------- #
def image_upload_path(instance, filename):
    # Example upload path
    return f"why_us/{filename}"

class why_us(models.Model):
    why_us_icon = models.ImageField(upload_to=image_upload_path)
    why_us_title = models.TextField(max_length=60)
    why_us_desc = models.TextField(max_length=500)
    mandatory_field = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.why_us_title} - {self.why_us_desc[:50]} ..."

    def clean(self):
        super().clean()  # Run default validations first

        # Validate why_us_icon
        if self.why_us_icon:
            valid_extensions = ['svg', 'png']
            extension = self.why_us_icon.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise ValidationError({
                    'why_us_icon': "Unsupported icon format. Only SVG allowed."
                })








# -------------------------------  Contact Form Secion Model ---------------------------------- #
class Contact_Us(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    tel = models.CharField(max_length=15)
    message = models.TextField(max_length=2000)
    mandatory_field = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    def clean(self):
        super().clean()

        # Honeypot validation: mandatory_field must be empty
        if self.mandatory_field:
            raise ValidationError("Mandatory field must be empty (spam check).")

        # Basic validations
        if not self.name:
            raise ValidationError({'name': "Name cannot be empty."})
        if not self.email:
            raise ValidationError({'email': "Email cannot be empty."})
        if not self.tel:
            raise ValidationError({'tel': "Telephone cannot be empty."})
        if not self.message:
            raise ValidationError({'message': "Message cannot be empty."})