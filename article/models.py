from django.db import models

# For user relationship with reviews
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=256)
    cover_image = models.ImageField(upload_to="article/images/")
    body = models.TextField(null=True)

    modifiedAt = models.DateTimeField(auto_now=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    
    featured = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    createdAt = models.DateTimeField(auto_now=True)

    # Relationship -> one to many
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    