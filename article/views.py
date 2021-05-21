from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Review
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# EDITING AND DELETING ARTICLE IMPORT - CLASS BASED VIEWS
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from article.models import Article
from django.urls import reverse
from django.http import HttpResponseRedirect

from article import models

# Create your views here.
def index(request):
    articles = Article.objects.filter(featured=True).order_by("-createdAt")

    context = {
        "articles": articles
    }

    return render(request, "article/index.html", context)


@login_required
def articles(request):

    articles = Article.objects.all().order_by("-createdAt")

    # Pagination
    paginator = Paginator(articles, 3)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    totalNum = page_obj.paginator.num_pages

    context = {
        "page_obj": page_obj,
        "range": range(1, totalNum+1),
    }


    return render(request, "article/articles.html", context)


@login_required
def articleDetail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    reviews = Review.objects.filter(article = article).order_by("-createdAt")

    context = {
        "article": article,
        "reviews": reviews
    }

    # To get rid of error of review passed in below function
    if 'error' in request.session:
        if request.session['count'] == 1:
            del request.session['error']
            del request.session['count']

    request.session['count'] = 1

    return render(request, "article/articleDetail.html", context)


# @login_required 
# def createArticle(request):
#     if request.method == "GET":
#         return render(request, "article/create-article.html")

#     if request.method == "POST":
#         title = request.POST['title']
#         body = request.POST['body']
#         user = request.user
#         cover_image = request.FILES['cover_image']

#         Article.objects.create(title=title, body=body, cover_image=cover_image, user=user)

#         return redirect("/article/create")


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'cover_image', 'body']
    template_name = 'article/create-article.html'

    # To pass in fields that are not in template but are required, like user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # Where to go after the Article is created
    def get_success_url(self):
        return reverse("article.articles") 


# EDITING AND DELETING ARTICLE
class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'cover_image', 'body']
    template_name = 'article/update-article.html'

    # Where to go after the Article is created
    def get_success_url(self):
        return reverse("user.own_profile", kwargs={'username': self.request.user.username}) 



class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article/delete-article.html'

    def get_success_url(self):
        return reverse("user.own_profile", kwargs={'username': self.request.user.username}) 




def submitReview(request):
    if request.method == "POST":
        title = request.POST['reviewTitle']
        body = request.POST['reviewBody']

        articleID = request.POST['articleID']
        article = Article.objects.get(id=articleID)

        reviewsOfUser = Review.objects.filter(user=request.user, article=article)
        reviewCount = reviewsOfUser.count()

        if reviewCount == 0:
            Review.objects.create(title=title, body=body, user= request.user, article=article)
        else:
            request.session['error'] = "You can only provide one review"
            request.session['count'] = 0
        
        return redirect(request.META['HTTP_REFERER'] + '#reviews') # request.META['HTTP_REFERER'] -> redirects to same page


def reviewUpdate(request, pk):
    if request.method == "POST":
        pk = request.POST['id']
        title = request.POST['title']
        body = request.POST['body']

        review = Review.objects.get(pk=pk)

        review.title = title
        review.body = body

        review.save()

        return HttpResponseRedirect(reverse("user.own_profile", kwargs={'username': request.user.username} ))

    else:
        review = Review.objects.get(pk=pk)
        print(review)
        context = {
            'review': review
        }
        return render(request,'article/review-update.html', context)


class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'article/review-delete.html'

    def get_success_url(self):
        return reverse("user.own_profile", kwargs={'username': self.request.user.username}) 
