from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path("sign-up/", views.signUpUser, name="user.sign-up"),
    path("log-out/", views.logOutUser),
    path("log-in/", views.logInUser, name="user.log-in"),
    
    path("user/<str:username>", views.userProfile, name="user.user_profile"),
]
