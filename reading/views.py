from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.decorators import teacher_required
from . import models

from utils.text_to_html import convert

@teacher_required
def reading_list(request):
    reading = models.ReadingPassage.objects.all()
    return render(request, 'reading/reading_list.html', {'reading': reading})

@teacher_required
def reading_detail(request, pk):
    reading_detail = models.ReadingPassage.objects.get(pk=pk)
    return render(request, 'reading/reading_detail.html', {'reading_detail': reading_detail})

@login_required
def student_reading_test_view(request, pk):
    reading = get_object_or_404(models.ReadingPassage, pk=pk)
    question = convert(reading.question_text)
    passage = convert(reading.passage_text)

    return render(request, 'reading/student_reading_view.html', {'reading' : reading, 'question' : question, 'passage' : passage})
