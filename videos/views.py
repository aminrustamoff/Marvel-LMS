from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from accounts.decorators import teacher_required, student_required, TeacherRequiredMixin

from .utils import youtube_id_extracter

from .models import ListeningPodcast
from assignments.models import PodcastTask
from progress.models import StudentProgress, ProgressPodcast

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import ListeningPodcastForm, DeleteConfirmForm
from .models import ListeningPodcast

@teacher_required
def video_list(request):
    videos = ListeningPodcast.objects.all().order_by('-created_at')
    paginator = Paginator(videos, 25)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'videos/video_list.html', {'page_obj': page_obj})

@teacher_required
def video_detail(request, pk):
    video = ListeningPodcast.objects.get(pk=pk)
    youtube_id = youtube_id_extracter.extract_youtube_id(video.url)
    return render(request, 'videos/video_detail.html', {'podcast': video, 'youtube_id' : youtube_id})

@student_required
def student_podcast_view(request, group_pk, assignment_pk, task_pk):
    group = request.user.student_groups.get(pk=group_pk)
    assignment = group.assignment_distributions.get(pk=assignment_pk)
    task = assignment.assignment.podcast_tasks.get(task_id=task_pk)
    podcast = task.task

    if request.method == "POST":
        student_progress, _ = StudentProgress.objects.get_or_create(
            user=request.user,
            group=group,
            assignment=assignment_pk
        )

        ProgressPodcast.objects.update_or_create(
            progress=student_progress,
            podcast=podcast,
            defaults={"is_seen" : True, "seen_at" : timezone.now()},        
        )

        return redirect("assignment:student_assignment_detail", group_pk=group.pk, assignment_pk=assignment.pk)


    youtube_id = youtube_id_extracter.extract_youtube_id(podcast.url)

    return render(request, 'videos/student_video_view.html', {'group' : group, 'podcast' : podcast, 'youtube_id' : youtube_id, 'assignment' : assignment})


class VideoCreateView(TeacherRequiredMixin, CreateView):
    model = ListeningPodcast
    form_class = ListeningPodcastForm
    template_name = "videos/video_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object.title}" was created.')
        return response

    def get_success_url(self):
        return reverse("podcast:video_detail", kwargs={"pk": self.object.pk})


class VideoUpdateView(TeacherRequiredMixin, UpdateView):
    model = ListeningPodcast
    form_class = ListeningPodcastForm
    template_name = "videos/video_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object.title}" was updated.')
        return response

    def get_success_url(self):
        return reverse("podcast:video_detail", kwargs={"pk": self.object.pk})


class VideoDeleteView(TeacherRequiredMixin, DeleteView):
    model = ListeningPodcast
    template_name = "videos/video_confirm_delete.html"
    success_url = reverse_lazy("podcast:video_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["confirm_form"] = DeleteConfirmForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        confirm_form = DeleteConfirmForm(request.POST, user=request.user)

        if confirm_form.is_valid():
            title = self.object.title
            self.object.delete()
            messages.success(request, f'"{title}" was deleted.')
            return redirect(self.success_url)

        context = self.get_context_data(confirm_form=confirm_form)
        return self.render_to_response(context)