from django.shortcuts import get_object_or_404, render

from .models import Group


def group_list(request):
    groups = Group.objects.prefetch_related("members").all()
    return render(request, "groups/group_list.html", {"groups": groups})


def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, "groups/group_detail.html", {"group": group})
