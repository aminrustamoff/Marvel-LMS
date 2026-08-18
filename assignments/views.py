from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from accounts.decorators import student_required, teacher_required, TeacherRequiredMixin    

from .models import *
from .forms import AssignmentForm

from django.contrib import messages
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView



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



class AssignmentTaskSyncMixin:
    """Syncs the four task-through tables to match what was selected in the form."""

    task_specs = [
        ("articles", ArticleTask),
        ("passages", PassageTask),
        ("listenings", ListeningTask),
        ("podcasts", PodcastTask),
    ]

    def sync_tasks(self, assignment, form):
        for field_name, model in self.task_specs:
            selected_ids = {obj.pk for obj in form.cleaned_data.get(field_name, [])}
            existing_qs = model.objects.filter(assignment=assignment)
            existing_ids = set(existing_qs.values_list("task_id", flat=True))

            to_remove = existing_ids - selected_ids
            if to_remove:
                existing_qs.filter(task_id__in=to_remove).delete()

            to_add = selected_ids - existing_ids
            if to_add:
                model.objects.bulk_create(
                    [model(assignment=assignment, task_id=task_id) for task_id in to_add]
                )


class AssignmentCreateView(TeacherRequiredMixin, AssignmentTaskSyncMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = "assignments/assignment_form.html"

    @transaction.atomic
    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        response = super().form_valid(form)
        self.sync_tasks(self.object, form)
        messages.success(self.request, f'Assignment "{self.object.title}" was created.')
        return response

    def get_success_url(self):
        return reverse("assignment:assignment_detail", kwargs={"pk": self.object.pk})


class AssignmentUpdateView(TeacherRequiredMixin, AssignmentTaskSyncMixin, UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = "assignments/assignment_form.html"

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        self.sync_tasks(self.object, form)
        messages.success(self.request, f'Assignment "{self.object.title}" was updated.')
        return response

    def get_success_url(self):
        return reverse("assignment:assignment_detail", kwargs={"pk": self.object.pk})


class AssignmentDeleteView(TeacherRequiredMixin, DeleteView):
    model = Assignment
    template_name = "assignments/assignment_confirm_delete.html"
    success_url = reverse_lazy("assignment:assignment_list")

    def form_valid(self, form):
        messages.success(self.request, f'Assignment "{self.object.title}" was deleted.')
        return super().form_valid(form)