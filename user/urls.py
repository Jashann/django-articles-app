from django.urls import path
from . import views

urlpatterns = [
    path("sign-up/", views.signUpUser, name="user.sign-up"),
    path("log-out/", views.logOutUser),
    path("log-in/", views.logInUser, name="user.log-in"),
]
