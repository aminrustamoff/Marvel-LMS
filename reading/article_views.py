from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from accounts.decorators import teacher_required, student_required, TeacherRequiredMixin

from . import models
from assignments.models import ArticleTask
from progress.models import StudentProgress, ProgressArticle

from .forms import ReadingArticleForm, ReadingArticleImageFormSet, DeleteConfirmForm

from django.contrib import messages
from django.contrib.auth import authenticate
from django.db import transaction
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, UpdateView


@teacher_required
def article_list(request):
    articles = models.ReadingArticle.objects.all()
    return render(request, 'articles/article_list.html', {'articles': articles})

@teacher_required
def article_detail(request, pk):
    article = models.ReadingArticle.objects.get(pk=pk)
    return render(request, 'articles/article_detail.html', {'article': article})

@login_required
def student_article_view(request, assignment_pk, pk):
    article_task = get_object_or_404(
        ArticleTask,
        assignment_id=assignment_pk,
        task_id=pk,
    )
    article = article_task.task
    assignment = article_task.assignment

    return render(request, 'articles/student_article_view.html', {'article' : article, 'assignment_pk' : assignment_pk, 'assignment' : assignment})


@login_required
@student_required
def mark_as_read(request, assignment_pk, pk):
    article = get_object_or_404(models.ReadingArticle, pk=pk)
    assignment = get_object_or_404(
                                    ArticleTask, 
                                    assignment_id=assignment_pk, 
                                    task=article).assignment

    if request.method == "POST":
        # ProgressReading modeliga saqlash
        student_progress, _ = StudentProgress.objects.get_or_create(
            user=request.user,
            assignment=assignment_pk,  # sizning bog'lanishingizga moslang
        )
        ProgressArticle.objects.update_or_create(
            progress=student_progress,
            article=article,
            defaults={"is_read" : True,  "read_at": timezone.now()},
        )

        return redirect("assignment:student_assignment_detail", pk=assignment.pk)

    return render(request, "articles/student_article_view.html", {"article": article})



class ReadingArticleCreateView(TeacherRequiredMixin, CreateView):
    model = models.ReadingArticle
    form_class = ReadingArticleForm
    template_name = "articles/article_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["formset"] = ReadingArticleImageFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            ctx["formset"] = ReadingArticleImageFormSet()
        ctx["is_edit"] = False
        return ctx

    @transaction.atomic
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        ctx = self.get_context_data()
        formset = ctx["formset"]

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, "The article has been added successfully.")
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("article:article_detail", kwargs={"pk": self.object.pk})


class ReadingArticleUpdateView(TeacherRequiredMixin, UpdateView):
    model = models.ReadingArticle
    form_class = ReadingArticleForm
    template_name = "articles/article_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["formset"] = ReadingArticleImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            ctx["formset"] = ReadingArticleImageFormSet(instance=self.object)
        ctx["is_edit"] = True
        return ctx

    @transaction.atomic
    def form_valid(self, form):
        ctx = self.get_context_data()
        formset = ctx["formset"]

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, "The article has been updated.")
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("article:article_detail", kwargs={"pk": self.object.pk})


class ReadingArticleDeleteView(TeacherRequiredMixin, View):
    """Parol tasdiqlash bilan o'chirish (avvalgi user delete view patterniga o'xshash)."""
    template_name = "articles/article_confirm_delete.html"

    def get_object(self):
        from django.shortcuts import get_object_or_404
        return get_object_or_404(models.ReadingArticle, pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        from django.shortcuts import render
        article = self.get_object()
        form = DeleteConfirmForm()
        return render(request, self.template_name, {"article": article, "form": form})

    def post(self, request, *args, **kwargs):
        from django.shortcuts import render, redirect
        article = self.get_object()
        form = DeleteConfirmForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["password"]
            user = authenticate(username=request.user.username, password=password)
            if user is not None:
                article.delete()
                messages.success(request, "The article has been deleted.")
                return redirect("article:article_list")
            form.add_error("password", "Password is incorrect.")

        return render(request, self.template_name, {"article": article, "form": form})




