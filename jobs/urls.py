# jobs/urls.py
from django.urls import path
from .views import (
    JobListView,
    JobDetailView,
    JobCreateView,
    JobUpdateView,
    JobDeleteView,
)

urlpatterns = [
    path("", JobListView.as_view(), name="job_list"),
    path("post/new/", JobCreateView.as_view(), name="job_create"),
    path("post/<slug:slug>/edit/", JobUpdateView.as_view(), name="job_edit"),
    path("post/<slug:slug>/delete/", JobDeleteView.as_view(), name="job_delete"),
    path("job/<slug:slug>/", JobDetailView.as_view(), name="job_detail"),
]
