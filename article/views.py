from django.shortcuts import render, get_object_or_404
from .models import Article
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "article/index.html")


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

    context = {
        "article": article
    }
    
    return render(request, "article/articleDetail.html", context)