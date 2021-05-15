from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("articles/", views.articles, name="article.articles"),
    path("article/<int:article_id>", views.articleDetail, name="article.article_detail"),
    path("article/create", views.createArticle, name="article.create_article"),

    path("article/submit-review", views.submitReview, name="article.submit_review" ),
    
]
