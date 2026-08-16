from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from accounts.decorators import teacher_required

from .utils import youtube_id_extracter

from .models import ListeningPodcast

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
def student_podcast_view(request, pk):
    podcast = get_object_or_404(ListeningPodcast, pk=pk)
    youtube_id = youtube_id_extracter.extract_youtube_id(podcast.url)

    return render(request, 'videos/student_video_view.html', {'podcast' : podcast, 'youtube_id' : youtube_id})