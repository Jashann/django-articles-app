from article.models import Article, Review
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def signUpUser(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            context = {
                "error": "Passwords don't match"
            }
            return render(request, "user/sign-up.html", context)
        elif len(password2) < 6:
            context = {
                "error": "Password should be at least 6 characters"
            }
            return render(request, "user/sign-up.html", context)
        
        # Passwords match and are at least 6 characters
        
        if User.objects.filter(email=email).exists():
            context = {
                "error": "Email is already in use"
            }
            return render(request, "user/sign-up.html", context)
        
        try: # creating user
            user = User.objects.create_user(username, email, password1)
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            return redirect("/")
        except IntegrityError: # username already exists
            context = {
                "error": "Username is already taken"
            }
            return render(request, "user/sign-up.html", context)


    # If it is GET request
    else:
        return render(request, "user/sign-up.html")


def logOutUser(request):
    logout(request)
    return redirect("/")


def logInUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']

        if "@" not in username:
            user = authenticate(request, username=username, password = password1)
        else:
            email = username
            user = authenticate(request, email=email, password = password1)

        if user is not None: # User is logged in this block
            login(request, user)

            # Taken from "https://stackoverflow.com/questions/38431166/redirect-to-next-after-login-in-django"
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect("/")
        else:
            context = {
                "error": "Invalid username or password"
            }
            return render(request, 'user/log-in.html', context)
    
    else:
        return render(request, "user/log-in.html")


def userProfile(request, username):
    user = User.objects.get(username=username)
    articles = Article.objects.filter(user=user)
    reviews = Review.objects.filter(user=user)
    
    context = {
        'user': user,
        'articles': articles,
        'reviews': reviews,
    }


    return render(request, "user/profile.html", context)