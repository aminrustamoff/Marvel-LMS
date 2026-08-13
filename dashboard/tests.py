from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class DashboardAccessTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher",
            password="secret123",
            role=User.Role.TEACHER,
        )
        self.student = User.objects.create_user(
            username="student",
            password="secret123",
            role=User.Role.STUDENT,
        )

    def test_teacher_can_access_teacher_dashboard(self):
        self.client.force_login(self.teacher)
        response = self.client.get(reverse("dashboard:teacher_dashboard"))

        self.assertEqual(response.status_code, 200)

    def test_student_cannot_access_teacher_dashboard(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("dashboard:teacher_dashboard"))

        self.assertEqual(response.status_code, 403)

    def test_student_login_redirects_to_student_dashboard(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "student", "password": "secret123"},
            follow=False,
        )

        self.assertRedirects(response, reverse("dashboard:student_dashboard"))

    def test_teacher_login_redirects_to_teacher_dashboard(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "teacher", "password": "secret123"},
            follow=False,
        )

        self.assertRedirects(response, reverse("dashboard:teacher_dashboard"))
