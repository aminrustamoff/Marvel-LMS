from django.shortcuts import render
from . import models

def listening_list(request):
    listening = models.Listening.objects.all()
    return render(request, 'listening/listening_list.html', {'listening': listening})

def listening_detail(request, pk):
    listening_detail = models.Listening.objects.get(pk=pk)
    return render(request, 'listening/listening_detail.html', {'listening_detail': listening_detail})