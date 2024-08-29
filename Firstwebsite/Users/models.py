from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to= 'profile_picture')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        image = Image.open(self.image.path)
        if image.height > 300 and image.width > 300:
            output_size = (200, 200)
            image.thumbnail(output_size)
            image = Image.open(self.image.path)