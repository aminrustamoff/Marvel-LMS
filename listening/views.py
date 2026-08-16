from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from accounts.decorators import teacher_required

from utils import text_to_html

from . import models
from assignments.models import ListeningTask
from progress.models import StudentProgress, ProgressListening

@teacher_required
def listening_list(request):
    listening = models.Listening.objects.all()
    return render(request, 'listening/listening_list.html', {'listening': listening})

@teacher_required
def listening_detail(request, pk):
    listening = get_object_or_404(models.Listening, pk=pk)
    
    question = text_to_html.convert(listening.question)

    return render(request, 'listening/listening_detail.html', {'listening' : listening, 'question' : question})

@login_required
def student_listening_view(request, assignment_pk, pk):
    listening_task = get_object_or_404(
        ListeningTask,
        assignment_id=assignment_pk,
        task_id=pk
    )

    assignment = listening_task.assignment
    listening = listening_task.task

    if request.method == "POST":

        answers ={}
        for key, value in request.POST.items():
            if key.startswith("question"):
                answers[key] = value

        student_progress, _ = StudentProgress.objects.get_or_create(
            user=request.user,
            assignment=assignment.pk,
        )

        ProgressListening.objects.update_or_create(
            progress=student_progress,
            listening_test=listening,
            defaults={'answers' : answers, 'submitted_at': timezone.now()}
        )

        return redirect("assignment:student_assignment_detail", assignment.pk)

    question = text_to_html.convert(listening.question)

    return render(request, 'listening/student_listening_view.html', {'listening' : listening, 'question' : question, 'assignment' : assignment})