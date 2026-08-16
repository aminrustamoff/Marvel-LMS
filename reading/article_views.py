from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from accounts.decorators import teacher_required, student_required

from . import models
from assignments.models import ArticleTask
from progress.models import StudentProgress, ProgressArticle

@teacher_required
def article_list(request):
    articles = models.ReadingArticle.objects.all()
    return render(request, 'articles/article_list.html', {'articles': articles})

@teacher_required
def article_detail(request, pk):
    article = models.ReadingArticle.objects.get(pk=pk)
    return render(request, 'articles/article_detail.html', {'article': article})

@login_required
def student_article_view(request, assignment_pk, pk):
    article_task = get_object_or_404(
        ArticleTask,
        assignment_id=assignment_pk,
        task_id=pk,
    )
    article = article_task.task
    assignment = article_task.assignment

    return render(request, 'articles/student_article_view.html', {'article' : article, 'assignment_pk' : assignment_pk, 'assignment' : assignment})


@login_required
@student_required
def mark_as_read(request, assignment_pk, pk):
    article = get_object_or_404(models.ReadingArticle, pk=pk)
    assignment = get_object_or_404(
                                    ArticleTask, 
                                    assignment_id=assignment_pk, 
                                    task=article).assignment

    if request.method == "POST":
        # ProgressReading modeliga saqlash
        student_progress, _ = StudentProgress.objects.get_or_create(
            user=request.user,
            assignment=assignment_pk,  # sizning bog'lanishingizga moslang
        )
        ProgressArticle.objects.update_or_create(
            progress=student_progress,
            article=article,
            defaults={"is_read" : True,  "read_at": timezone.now()},
        )

        return redirect("assignment:student_assignment_detail", pk=assignment.pk)

    return render(request, "articles/student_article_view.html", {"article": article})