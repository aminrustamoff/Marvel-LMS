from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from accounts.decorators import teacher_required, student_required

from .utils import youtube_id_extracter

from .models import ListeningPodcast
from assignments.models import PodcastTask
from progress.models import StudentProgress, ProgressPodcast

@teacher_required
def video_list(request):
    videos = ListeningPodcast.objects.all()
    return render(request, 'videos/video_list.html', {'videos': videos})

@teacher_required
def video_detail(request, pk):
    video = ListeningPodcast.objects.get(pk=pk)
    youtube_id = youtube_id_extracter.extract_youtube_id(video.url)
    return render(request, 'videos/video_detail.html', {'podcast': video, 'youtube_id' : youtube_id})

@login_required
@student_required
def student_podcast_view(request, assignment_pk, pk):
    podcast_task = get_object_or_404(
        PodcastTask,
        assignment_id=assignment_pk,
        task_id = pk,
    )

    podcast = podcast_task.task
    assignment = podcast_task.assignment

    if request.method == "POST":
        student_progress, _ = StudentProgress.objects.get_or_create(
            user=request.user,
            assignment=assignment_pk
        )

        ProgressPodcast.objects.update_or_create(
            progress=student_progress,
            podcast=podcast,
            defaults={"is_seen" : True, "seen_at" : timezone.now()},        
        )

        return redirect("assignment:student_assignment_detail", pk=assignment.pk)


    youtube_id = youtube_id_extracter.extract_youtube_id(podcast.url)

    return render(request, 'videos/student_video_view.html', {'podcast' : podcast, 'youtube_id' : youtube_id, 'assignment' : assignment})