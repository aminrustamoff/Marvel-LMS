from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from accounts.decorators import student_required, teacher_required, TeacherRequiredMixin    

from .models import *
from .forms import AssignmentForm, AssignmentDistributionForm, DeleteConfirmForm

from django.contrib import messages
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView



@teacher_required
def assignment_list(request):
    search = request.GET.get("search", "").strip()

    assignments = Assignment.objects.all()

    if search:
        assignments = assignments.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    assignments = assignments.order_by("-created_at")

    paginator = Paginator(assignments, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'assignments/assignment_list.html',
        {
            'assignments': assignments,
            'page_obj': page_obj,
            'search': search,
        }
    )

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

@student_required
def student_assignment_detail(request, group_pk, assignment_pk):
    try:
        group = request.user.student_groups.get(pk=group_pk)
        assignment = group.assignment_distributions.get(pk=assignment_pk).assignment
        assignment_pk = group.assignment_distributions.get(pk=assignment_pk).pk

        listening_tasks = assignment.listening_tasks.all()
        podcast_tasks = assignment.podcast_tasks.all()
        article_tasks = assignment.article_tasks.all()
        passage_tasks = assignment.passage_tasks.all()

        content = {
            'group' : group,
            'assignment': assignment,
            'assignment_pk' : assignment_pk,
            'listening_tasks': listening_tasks,
            'podcast_tasks': podcast_tasks,
            'article_tasks': article_tasks,
            'passage_tasks': passage_tasks,
        }
        return render(request, 'assignments/student_assignment_detail.html', content)
    except Exception as e:
        return HttpResponse("<h1>Something went wrong (404)</h1>")



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





class AssignmentDistributionCreateView(TeacherRequiredMixin, CreateView):
    model = AssignmentDistribution
    form_class = AssignmentDistributionForm
    template_name = "assignments/assignment_group_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.assignment = get_object_or_404(Assignment, pk=self.kwargs["assignment_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["assignment"] = self.assignment
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assignment"] = self.assignment
        return context

    def form_valid(self, form):
        form.instance.assignment = self.assignment
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object.group.name}" was added to this assignment.')
        return response

    def get_success_url(self):
        return reverse("assignment:assignment_detail", kwargs={"pk": self.assignment.pk})


class AssignmentDistributionUpdateView(TeacherRequiredMixin, UpdateView):
    model = AssignmentDistribution
    form_class = AssignmentDistributionForm
    template_name = "assignments/assignment_group_form.html"
    pk_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):
        self.assignment = get_object_or_404(Assignment, pk=self.kwargs["assignment_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return AssignmentDistribution.objects.filter(assignment=self.assignment)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["assignment"] = self.assignment
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assignment"] = self.assignment
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object.group.name}" link was updated.')
        return response

    def get_success_url(self):
        return reverse("assignment:assignment_detail", kwargs={"pk": self.assignment.pk})


class AssignmentDistributionDeleteView(TeacherRequiredMixin, DeleteView):
    model = AssignmentDistribution
    template_name = "assignments/assignment_group_confirm_delete.html"
    pk_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):
        self.assignment = get_object_or_404(Assignment, pk=self.kwargs["assignment_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return AssignmentDistribution.objects.filter(assignment=self.assignment)

    def get_success_url(self):
        return reverse("assignment:assignment_detail", kwargs={"pk": self.assignment.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assignment"] = self.assignment
        context["confirm_form"] = DeleteConfirmForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        confirm_form = DeleteConfirmForm(request.POST, user=request.user)

        if confirm_form.is_valid():
            group_name = self.object.group.name
            self.object.delete()
            messages.success(request, f'"{group_name}" was removed from this assignment.')
            return redirect(self.get_success_url())

        context = self.get_context_data(confirm_form=confirm_form)
        return self.render_to_response(context)