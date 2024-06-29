from django.db import models
from django.contrib.auth.models import AbstractUser

class OCRImage(models.Model):
    image = models.ImageField(upload_to='images/')
    extracted_text = models.TextField(blank=True)
    bold_words = models.TextField(blank=True)
    image_base64 = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OCRImage {self.id}"


class CustomUser(AbstractUser):
    pass
