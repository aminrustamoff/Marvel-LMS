from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from accounts.decorators import teacher_required, student_required
from . import models
from progress.models import StudentProgress, ProgressReading
from assignments.models import PassageTask

from utils.text_to_html import convert

@teacher_required
def reading_list(request):
    reading = models.ReadingPassage.objects.all()
    return render(request, 'reading/reading_list.html', {'reading': reading})

@teacher_required
def reading_detail(request, pk):
    reading = models.ReadingPassage.objects.get(pk=pk)
    question = convert(reading.question_text)
    passage = convert(reading.passage_text)
    return render(request, 'reading/reading_detail.html', {'reading': reading, 'question' : question, 'passage' : passage})

@login_required
@student_required
def student_reading_test_view(request, assignment_pk, pk):
    reading_task = get_object_or_404(
        PassageTask,
        assignment_id=assignment_pk,
        task_id=pk,
        
    )
    reading = reading_task.task
    assignment = reading_task.assignment
    question = convert(reading.question_text)
    passage = convert(reading.passage_text)

    return render(request, 'reading/student_reading_view.html', {'reading' : reading, 'question' : question, 'passage' : passage, 'assignment' : assignment})


@login_required
@student_required
def submit_answers(request, assignment_pk, pk):
    reading_task = get_object_or_404(
        PassageTask,
        assignment_id=assignment_pk,
        task_id=pk,
    )

    reading = reading_task.task

    if request.method == "POST":
        answers = {}
        for key, value in request.POST.items():
            if key.startswith("question"):
                # key masalan: "question1", "question2" ...
                answers[key] = value

        # ProgressReading modeliga saqlash
        student_progress, _ = StudentProgress.objects.get_or_create(
            user=request.user,
            assignment=reading_task.assignment,  # sizning bog'lanishingizga moslang
        )
        ProgressReading.objects.update_or_create(
            progress=student_progress,
            passage=reading,
            defaults={"answers": answers, "submitted_at": timezone.now()},
        )

        return redirect("reading:result", pk=reading_task.assignment.pk)

    
    assignment = reading_task.assignment
    question = convert(reading.question_text)
    passage = convert(reading.passage_text)

    return render(request, 'reading/student_reading_view.html', {'reading' : reading, 'question' : question, 'passage' : passage, 'assignment' : assignment})


@login_required
@student_required
def student_reading_result(request, pk):
    return redirect("assignment:student_assignment_detail", pk=pk)
