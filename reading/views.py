from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from accounts.decorators import teacher_required, student_required, TeacherRequiredMixin
from . import models
from progress.models import StudentProgress, ProgressReading
from assignments.models import PassageTask

from utils.text_to_html import convert

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import ReadingPassageForm, ReadingPassageImageFormSet, DeleteConfirmForm
from .models import ReadingPassage


@teacher_required
def reading_list(request):
    reading = models.ReadingPassage.objects.all().order_by('-created_at')
    paginator = Paginator(reading, 25)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'reading/reading_list.html', {'page_obj': page_obj})

@teacher_required
def reading_detail(request, pk):
    reading = models.ReadingPassage.objects.get(pk=pk)
    question = convert(reading.question_text)
    passage = convert(reading.passage_text)
    return render(request, 'reading/reading_detail.html', {'reading': reading, 'question' : question, 'passage' : passage})

@student_required
def student_reading_test_view(request, group_pk, assignment_pk, task_pk):
    group = request.user.student_groups.get(pk=group_pk)
    assignment = group.assignment_distributions.get(pk=assignment_pk)
    task = assignment.assignment.passage_tasks.get(task_id=task_pk)
    reading = task.task

    if request.method == "POST":
            answers = {}
            for key, value in request.POST.items():
                if key.startswith("question"):
                    # key masalan: "question1", "question2" ...
                    answers[key] = value
    
            # ProgressReading modeliga saqlash
            student_progress, _ = StudentProgress.objects.get_or_create(
                user=request.user,
                group=group,
                assignment=assignment,  # sizning bog'lanishingizga moslang
            )
            ProgressReading.objects.update_or_create(
                progress=student_progress,
                passage=reading,
                defaults={"answers": answers, "submitted_at": timezone.now()},
            )
    
            return redirect("assignment:student_assignment_detail", group_pk=group.pk , assignment_pk=assignment.pk)

    question = convert(reading.question_text)
    passage = convert(reading.passage_text)

    return render(request, 'reading/student_reading_view.html', {'group' : group, 'reading' : reading, 'question' : question, 'passage' : passage, 'assignment' : assignment})


class ReadingPassageFormsetMixin:
    """Handles the passage form + inline gallery-image formset together."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = ReadingPassageImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context["image_formset"] = ReadingPassageImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context["image_formset"]

        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            return super().form_valid(form)

        return self.render_to_response(self.get_context_data(form=form))


class ReadingPassageCreateView(TeacherRequiredMixin, ReadingPassageFormsetMixin, CreateView):
    model = ReadingPassage
    form_class = ReadingPassageForm
    template_name = "reading/reading_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        if response.status_code == 302:
            messages.success(self.request, f'"{self.object.title}" was created.')
        return response

    def get_success_url(self):
        return reverse("reading:reading_detail", kwargs={"pk": self.object.pk})


class ReadingPassageUpdateView(TeacherRequiredMixin, ReadingPassageFormsetMixin, UpdateView):
    model = ReadingPassage
    form_class = ReadingPassageForm
    template_name = "reading/reading_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        if response.status_code == 302:
            messages.success(self.request, f'"{self.object.title}" was updated.')
        return response

    def get_success_url(self):
        return reverse("reading:reading_detail", kwargs={"pk": self.object.pk})


class ReadingPassageDeleteView(TeacherRequiredMixin, DeleteView):
    model = ReadingPassage
    template_name = "reading/reading_confirm_delete.html"
    success_url = reverse_lazy("reading:reading_list")

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