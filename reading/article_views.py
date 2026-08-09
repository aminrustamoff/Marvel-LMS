from django.shortcuts import render

from . import models

def article_list(request):
    articles = models.ReadingArticle.objects.all()
    return render(request, 'articles/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = models.ReadingArticle.objects.get(pk=pk)
    return render(request, 'articles/article_detail.html', {'article': article})