from django.shortcuts import render, get_object_or_404
from accounts.decorators import teacher_required
from django.core.paginator import Paginator


from .models import StudentProgress
from assignments.models import Assignment, AssignmentDistribution
from groups.models import Group

def student_assignment_progress_view(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    students = group.members.all().order_by('-date_joined')
    progresses = [obj for obj in group.progress_groups.all()]

    all_assignments = group.assignment_distributions.all().order_by('-created_at')
    paginator = Paginator(all_assignments, 5)
    page_number = request.GET.get('page')
    assignments = paginator.get_page(page_number)

    context = {
        'group' : group,
        'students' : students,
        'assignments' : assignments,
        'progresses' : progresses
    }
    return render(request, 'progress/teacher_table_view.html', context)



