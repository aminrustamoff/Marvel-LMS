from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.decorators import teacher_required
from accounts.models import User
from groups.models import Group

from assignments.models import Assignment
from reading.models import ReadingArticle, ReadingPassage 
from listening.models import Listening
from videos.models import ListeningPodcast

@teacher_required
def teacher_dashboard(request):
    students_count = User.objects.filter(role=User.Role.STUDENT).count()
    teachers_count = User.objects.filter(role=User.Role.TEACHER).count()
    groups_count = Group.objects.count()

    assignments_count = Assignment.objects.count()
    reading_passages_count = ReadingPassage.objects.count()
    reading_articles_count = ReadingArticle.objects.count()
    listening_count = Listening.objects.count()
    videos_count = ListeningPodcast.objects.count()

    return render(request, "dashboard/index.html", {
        "students_count": students_count,
        "teachers_count": teachers_count,
        "groups_count": groups_count,

        "reading_articles_count": reading_articles_count,
        "reading_passages_count": reading_passages_count,
        "assignments_count": assignments_count,
        "listening_count": listening_count,
        "videos_count": videos_count,
    })

@login_required
def student_dashboard(request):
    return render(request, "dashboard/student_dashboard.html")
