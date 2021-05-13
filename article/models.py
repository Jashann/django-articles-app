from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=256)
    cover_image = models.ImageField(upload_to="article/images/")
    body = models.TextField(null=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    modifiedAt = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return self.title