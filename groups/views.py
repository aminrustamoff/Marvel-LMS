from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from accounts.decorators import teacher_required

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
