from django.urls import path
from . import views

urlpatterns = [

    # Applicant
    path("apply/<slug:slug>/", views.apply_to_job, name="apply_to_job"),
    path("my-applications/", views.my_applications, name="my_applications"),
    path("success/", views.application_success, name="application_success"),


    # Recruiter
    path("received-applications/", views.recruiter_applications, name="recruiter_applications"),
    path("update-status/<int:app_id>/",
         views.update_application_status, name="update_application_status"),
]
