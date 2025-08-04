from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import CustomUser
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='profiles/profile_pics', default='profiles/profile_pics/default.jpg',)
    slug = models.SlugField(blank=True, null=True, unique=True)
    
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)
        
        
        try:
            if self.avatar and os.path.isfile(self.avatar.path):
                img = Image.open(self.avatar.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.avatar.path)
        except Exception as e:
            # اگر پردازش تصویر با خطا مواجه شد، از کرش کردن جلوگیری می‌کنه
            print(f"خطا در پردازش تصویر پروفایل: {e}")

    
    def get_absolute_url(self):
        return reverse('profiles:detail', kwargs={'slug': self.slug})
