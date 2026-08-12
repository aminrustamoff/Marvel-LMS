from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from accounts.decorators import student_required, teacher_required

from .models import *

@teacher_required
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments})

@teacher_required
def assignment_detail(request, pk):
    assignment = Assignment.objects.get(pk=pk)
    listening_tasks = ListeningTask.objects.filter(assignment=assignment)
    podcast_tasks = PodcastTask.objects.filter(assignment=assignment)
    article_tasks = ArticleTask.objects.filter(assignment=assignment)
    passage_tasks = PassageTask.objects.filter(assignment=assignment)

    return render(request, 'assignments/assignment_detail.html', 
        {
            'assignment': assignment, 
            'listening_tasks': listening_tasks,
            'podcast_tasks': podcast_tasks,
            'article_tasks': article_tasks,
            'passage_tasks': passage_tasks,
        }
    )

@login_required
@student_required
def student_assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    if not assignment.group.members.filter(pk=request.user.pk).exists():
        raise PermissionDenied

    listening_tasks = ListeningTask.objects.filter(assignment=assignment)
    podcast_tasks = PodcastTask.objects.filter(assignment=assignment)
    article_tasks = ArticleTask.objects.filter(assignment=assignment)
    passage_tasks = PassageTask.objects.filter(assignment=assignment)

    content = {
        'assignment': assignment,
        'listening_tasks': listening_tasks,
        'podcast_tasks': podcast_tasks,
        'article_tasks': article_tasks,
        'passage_tasks': passage_tasks,
    }
    return render(request, 'assignments/student_assignment_detail.html', content)