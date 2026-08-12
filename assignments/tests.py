from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from groups.models import Group

from .models import Assignment


class StudentAssignmentAccessTests(TestCase):
    def setUp(self):
        self.teacher = get_user_model().objects.create_user(
            username="teacher",
            password="secret123",
            role="TEACHER",
        )
        self.student = get_user_model().objects.create_user(
            username="student",
            password="secret123",
            role="STUDENT",
        )
        self.group = Group.objects.create(name="Group A")
        self.group.members.add(self.student)

    def test_student_can_open_assigned_assignment(self):
        assignment = Assignment.objects.create(
            title="Assigned assignment",
            description="This is assigned to the student",
            group=self.group,
            assigned_by=self.teacher,
        )

        self.client.login(username="student", password="secret123")
        response = self.client.get(
            reverse("assignment:student_assignment_detail", kwargs={"pk": assignment.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_student_cannot_open_unassigned_assignment(self):
        other_group = Group.objects.create(name="Group B")
        assignment = Assignment.objects.create(
            title="Other assignment",
            description="This is not assigned to the student",
            group=other_group,
            assigned_by=self.teacher,
        )

        self.client.login(username="student", password="secret123")
        response = self.client.get(
            reverse("assignment:student_assignment_detail", kwargs={"pk": assignment.pk})
        )

        self.assertEqual(response.status_code, 403)
