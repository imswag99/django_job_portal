# jobs/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Job
from .forms import JobForm
from django.db.models import Q
from django.core.paginator import Paginator

# Utility mixin to ensure recruiter-only access
class RecruiterRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and getattr(user, "is_recruiter", False)

    def handle_no_permission(self):
        messages.error(self.request, "You must be a recruiter to access this page.")
        return redirect("login")

# Public job list with search/filter/pagination
class JobListView(ListView):
    model = Job
    template_name = "jobs/job_list.html"  # create this template when ready
    context_object_name = "jobs"
    paginate_by = 10

    def get_queryset(self):
        qs = Job.objects.filter(is_active=True).select_related("recruiter")
        q = self.request.GET.get("q")
        location = self.request.GET.get("location")
        job_type = self.request.GET.get("job_type")
        remote = self.request.GET.get("remote")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(requirements__icontains=q) | Q(company_name__icontains=q))
        if location:
            qs = qs.filter(location__icontains=location)
        if job_type:
            qs = qs.filter(job_type=job_type)
        if remote in ("1", "true", "True"):
            qs = qs.filter(remote=True)
        return qs.order_by("-posted_at")

# Public job detail
class JobDetailView(DetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"
    slug_field = "slug"
    slug_url_kwarg = "slug"

# Recruiter creates job
class JobCreateView(LoginRequiredMixin, RecruiterRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"

    def form_valid(self, form):
        job = form.save(commit=False)
        job.recruiter = self.request.user
        job.save()
        messages.success(self.request, "Job posted successfully.")
        return redirect(job.get_absolute_url())

# Recruiter updates job (only owner)
class JobUpdateView(LoginRequiredMixin, RecruiterRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def dispatch(self, request, *args, **kwargs):
        # ensure only the recruiter who owns it can edit
        self.object = self.get_object()
        if self.object.recruiter != request.user:
            messages.error(request, "You are not allowed to edit this job.")
            return redirect(self.object.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Job updated successfully.")
        return super().form_valid(form)

# Recruiter deletes job (soft delete or hard depending on policy)
class JobDeleteView(LoginRequiredMixin, RecruiterRequiredMixin, DeleteView):
    model = Job
    template_name = "jobs/job_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("job_list")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.recruiter != request.user:
            messages.error(request, "You are not allowed to delete this job.")
            return redirect(self.object.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)
