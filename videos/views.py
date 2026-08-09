from django.shortcuts import render

from .utils import youtube_id_extracter

from .models import ListeningPodcast

def video_list(request):
    videos = ListeningPodcast.objects.all()
    return render(request, 'videos/video_list.html', {'videos': videos})

def video_detail(request, pk):
    video = ListeningPodcast.objects.get(pk=pk)
    youtube_id = youtube_id_extracter.extract_youtube_id(video.url)
    return render(request, 'videos/video_detail.html', {'video': video, 'youtube_id' : youtube_id})
