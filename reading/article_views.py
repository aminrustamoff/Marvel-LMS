from django.shortcuts import render

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