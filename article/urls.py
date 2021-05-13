from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("articles", views.articles, name="article.articles"),
    path("article/<int:article_id>", views.articleDetail, name="article.article_detail" )
]
