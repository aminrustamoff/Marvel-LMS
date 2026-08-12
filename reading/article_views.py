from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from accounts.decorators import teacher_required

from . import models

@teacher_required
def article_list(request):
    articles = models.ReadingArticle.objects.all()
    return render(request, 'articles/article_list.html', {'articles': articles})

@teacher_required
def article_detail(request, pk):
    article = models.ReadingArticle.objects.get(pk=pk)
    return render(request, 'articles/article_detail.html', {'article': article})

@login_required
def student_article_view(request, pk):
    article = get_object_or_404(models.ReadingArticle, pk=pk)

    # if not article.objects.filter(pk=).e

    return render(request, 'articles/student_article_view.html', {'article' : article})