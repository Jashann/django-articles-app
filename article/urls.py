from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("articles/", views.articles, name="article.articles"),

    #Search
    path("articles/search", views.articleSearch, name="article.article_search"),

    path("article/create", views.ArticleCreateView.as_view(), name="article.create_article"),
    path("article/<int:article_id>", views.articleDetail, name="article.article_detail"),

    # Editing and Deleting article
    path("article/<int:pk>/edit", views.ArticleUpdateView.as_view(), name="article.article_update"),
    path("article/<int:pk>/delete", views.ArticleDeleteView.as_view(), name="article.article_delete"),

    path("article/submit-review", views.submitReview, name="article.submit_review" ),

    # Review
    path("article/review/<int:pk>/edit", views.reviewUpdate, name="article.review_update"),
    path("article/review/<int:pk>/delete", views.ReviewDeleteView.as_view(), name="article.review_delete")
    
]
