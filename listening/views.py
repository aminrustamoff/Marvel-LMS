from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from accounts.decorators import teacher_required

from utils import text_to_html

from . import models

@teacher_required
def listening_list(request):
    listening = models.Listening.objects.all()
    return render(request, 'listening/listening_list.html', {'listening': listening})

@teacher_required
def listening_detail(request, pk):
    listening_detail = models.Listening.objects.get(pk=pk)
    return render(request, 'listening/listening_detail.html', {'listening_detail': listening_detail})

@login_required
def student_listening_view(request, pk):
    listening = get_object_or_404(models.Listening, pk=pk)

    question = text_to_html.convert(listening.question)

    return render(request, 'listening/student_listening_view.html', {'listening' : listening, 'question' : question})