from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from article.models import Article, Review, Bookmark 

# EDITING AND DELETING ARTICLE IMPORT - CLASS BASED VIEWS
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    articles = Article.objects.filter(featured=True).order_by("-createdAt")
    bookmarked = []

    if request.user.is_authenticated:
        for article in articles:
            bookmarkObject = Bookmark.objects.filter(article=article, user = request.user)
            if bookmarkObject:
                bookmarked.append(article.id)
    
    context = {
        'articles': articles,
        'bookmarked': bookmarked
    }

    return render(request, "article/index.html", context)


def articles(request):

    articles = Article.objects.all().order_by("-createdAt")

    bookmarked = []

    # Pagination
    paginator = Paginator(articles, 3)

    page_number = request.GET.get("page")

    articles = paginator.get_page(page_number)

    totalNum = articles.paginator.num_pages

    if request.user.is_authenticated:
        for article in articles:
            bookmarkObject = Bookmark.objects.filter(article=article, user = request.user)
            if bookmarkObject:
                bookmarked.append(article.id)

    context = {
        "articles": articles,
        "range": range(1, totalNum+1),
        'bookmarked': bookmarked
    }


    return render(request, "article/articles.html", context)


def articleDetail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    bookmarked = False

    if request.user.is_authenticated:
        bookmarkObject = Bookmark.objects.filter(article=article, user = request.user)
        if bookmarkObject:
            bookmarked = True

    reviews = Review.objects.filter(article = article).order_by("-createdAt")

    context = {
        "article": article,
        "reviews": reviews,
        'bookmarked': bookmarked
    }

    # To get rid of error of review passed in below function
    if 'error' in request.session:
        if request.session['count'] == 1:
            del request.session['error']
            del request.session['count']

    request.session['count'] = 1

    return render(request, "article/articleDetail.html", context)

def articleSearch(request):
    searchText = request.GET['searchText']
    
    articles = Article.objects.filter(title__contains=searchText)

    users = User.objects.filter(username__contains=searchText)

    bookmarked = []

    for user in users:
        userArticles = Article.objects.filter(user=user)
        articles = articles.union(userArticles)

     # Pagination
    paginator = Paginator(articles, 3)

    page_number = request.GET.get("page")

    articles = paginator.get_page(page_number)

    totalNum = articles.paginator.num_pages

    if request.user.is_authenticated:
        for article in articles:
            bookmarkObject = Bookmark.objects.filter(article=article, user = request.user)
            if bookmarkObject:
                bookmarked.append(article.id)

    context = {
        "articles": articles,
        "range": range(1, totalNum+1),
        'bookmarked': bookmarked
    }

    return render(request, "article/articles.html", context)





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
    
    # To pass in fields that are not set like user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("article.articles") 

# EDITING AND DELETING ARTICLE
class ArticleUpdateView(LoginRequiredMixin, UpdateView):

    model = Article
    fields = ['title', 'cover_image', 'body']
    template_name = 'article/update-article.html'

    def get_queryset(self):
        queryset = super(ArticleUpdateView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def form_valid(self, form):
        return super().form_valid(form)

    # Where to go after the Article is created
    def get_success_url(self):
        return reverse("user.user_profile", kwargs={'username': self.request.user.username}) 


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'article/delete-article.html'

    def get_queryset(self):
        queryset = super(ArticleDeleteView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse("user.user_profile", kwargs={'username': self.request.user.username}) 



@login_required
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

@login_required
def reviewUpdate(request, pk):
    if request.method == "POST":

        pk = request.POST['id']
        title = request.POST['title']
        body = request.POST['body']

        review = Review.objects.get(pk=pk)

        review.title = title
        review.body = body

        review.save()

        return HttpResponseRedirect(reverse("user.user_profile", kwargs={'username': request.user.username} ))

    else: # GET REQUEST
        review = Review.objects.get(pk=pk)

        if not request.user == review.user:
            raise Http404

        context = {
            'review': review
        }
        return render(request,'article/review-update.html', context)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'article/review-delete.html'

    def get_success_url(self):
        return reverse("user.user_profile", kwargs={'username': self.request.user.username}) 

@login_required
def bookmark(request,pk):
    user = request.user
    article = Article.objects.get(pk=pk)

    bookmarkObject = Bookmark.objects.filter(article=article, user=user)

    if bookmarkObject:
        bookmarked = bookmarkObject[0]
        bookmarked.delete()
    else:
        Bookmark.objects.create(user=user, article=article)

    htmlID = "#"+ str(article.id)

    return redirect(request.META['HTTP_REFERER'] + htmlID)