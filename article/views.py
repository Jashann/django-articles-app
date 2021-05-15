from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Review
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    articles = Article.objects.filter(featured=True).order_by("-createdAt")

    context = {
        "articles": articles
    }

    return render(request, "article/index.html", context)


@login_required 
def createArticle(request):
    if request.method == "GET":
        return render(request, "article/create-article.html")



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
        
        return redirect(request.META['HTTP_REFERER'])