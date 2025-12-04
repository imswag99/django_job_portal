from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from jobs.models import Job
from .forms import ApplicationForm
from .models import Application


@login_required
def apply_to_job(request, slug):
    job = get_object_or_404(Job, slug=slug)

    if not request.user.is_applicant:
        messages.error(request, "Only applicants can apply to jobs.")
        return redirect("home")

    # Prevent duplicate applications
    if Application.objects.filter(applicant=request.user, job=job).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect("job_detail", slug=slug)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.job = job
            application.save()

            messages.success(request, "Your application has been submitted.")
            return redirect("application_success")
    else:
        form = ApplicationForm()

    return render(request, "applications/apply.html", {"form": form, "job": job})


@login_required
def my_applications(request):
    if not request.user.is_applicant:
        messages.error(request, "Only applicants can see their applications.")
        return redirect("home")

    applications = Application.objects.filter(applicant=request.user)

    return render(request, "applications/my_applications.html", {
        "applications": applications
    })

def application_success(request):
    return render(request, "applications/application_success.html")


@login_required
def recruiter_applications(request):
    if not request.user.is_recruiter:
        messages.error(request, "Only recruiters can see received applications.")
        return redirect("home")

    # Applications for jobs posted by this recruiter
    applications = Application.objects.filter(job__recruiter=request.user)

    return render(request, "applications/recruiter_applications.html", {
        "applications": applications
    })


@login_required
def update_application_status(request, app_id):
    if not request.user.is_recruiter:
        messages.error(request, "Only recruiters can update statuses.")
        return redirect("home")

    application = get_object_or_404(Application, pk=app_id)

    if application.job.recruiter != request.user:
        messages.error(request, "Unauthorized action.")
        return redirect("recruiter_applications")

    if request.method == "POST":
        status = request.POST.get("status")

        if status not in ["pending", "reviewed", "accepted", "rejected"]:
            messages.error(request, "Invalid status.")
            return redirect("recruiter_applications")

        application.status = status
        application.save()
        messages.success(request, f"Application updated to {status}.")

    return redirect("recruiter_applications")