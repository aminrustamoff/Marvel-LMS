from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.decorators import teacher_required
from . import models

@teacher_required
def reading_list(request):
    reading = models.ReadingPassage.objects.all()
    return render(request, 'reading/reading_list.html', {'reading': reading})

@teacher_required
def reading_detail(request, pk):
    reading_detail = models.ReadingPassage.objects.get(pk=pk)
    return render(request, 'reading/reading_detail.html', {'reading_detail': reading_detail})