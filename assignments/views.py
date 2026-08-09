from django.shortcuts import render

from .models import *

def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments})

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