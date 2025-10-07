from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    body = models.TextField()
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField(blank=True)
    screenshot = models.ImageField(upload_to='projects/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)  # ✅ moderation

    def __str__(self):
        return f'Comment by {self.author_name}'

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # admin must approve

    def __str__(self):
        return f"{self.name} - {self.created_at:%Y-%m-%d}"
