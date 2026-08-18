from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.decorators import teacher_required, TeacherRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .forms import GroupForm

from .models import Group
from assignments.models import *

@teacher_required
def group_list(request):
    groups = Group.objects.prefetch_related("members").all()
    return render(request, "groups/group_list.html", {"groups": groups})

@teacher_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, "groups/group_detail.html", {"group": group})

@login_required
def student_group_detail(request, pk):
    group = request.user.student_groups.get(pk=pk)
    members = Group.objects.filter(pk=group.pk)
    assignments = Assignment.objects.filter(pk=group.pk)
    return render(request, "groups/student_group_detail.html", {'group' : group, 'members' : members, 'assignments' : assignments})


class GroupCreateView(TeacherRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = "groups/group_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Group "{self.object.name}" created successfully.')
        return response

    def get_success_url(self):
        return reverse("groups:detail", kwargs={"pk": self.object.pk})


class GroupUpdateView(TeacherRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "groups/group_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Group "{self.object.name}" updated successfully.')
        return response

    def get_success_url(self):
        return reverse("groups:detail", kwargs={"pk": self.object.pk})


class GroupDeleteView(TeacherRequiredMixin, DeleteView):
    model = Group
    template_name = "groups/group_confirm_delete.html"
    success_url = reverse_lazy("groups:list")

    def form_valid(self, form):
        messages.success(self.request, f'Group "{self.object.name}" deleted successfully.')
        return super().form_valid(form)
