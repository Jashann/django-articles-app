from django.contrib import admin
from .models import Article, Review

# Register your models here.
admin.site.register([Article, Review])