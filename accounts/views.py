from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from applications.models import Application

# Create your views here.

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Users cannot self-register as admin
            if user.role == user.ADMIN:
                user.role = user.APPLICANT
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # ✅ Role-based redirection
            if user.is_superuser:
                return redirect('admin:index')
            elif hasattr(user, 'is_recruiter') and user.is_recruiter:
                return redirect('recruiter_dashboard')
            elif hasattr(user, 'is_applicant') and user.is_applicant:
                return redirect('applicant_dashboard')
            else:
                messages.error(request, "User role not assigned.")
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def recruiter_dashboard(request):
    if not request.user.is_recruiter:
        return redirect('home')

    # Fetch only jobs posted by this recruiter
    jobs = Job.objects.filter(recruiter=request.user)

    return render(request, 'accounts/recruiter_dashboard.html', {'jobs': jobs})

@login_required
def applicant_dashboard(request):
    user = request.user

    total_applications = Application.objects.filter(applicant=user).count()
    accepted_applications = Application.objects.filter(applicant=user, status="accepted").count()
    rejected_applications = Application.objects.filter(applicant=user, status="rejected").count()

    # Jobs applied by this applicant
    applications = Application.objects.filter(applicant=user).select_related('job')

    # Optional: Recommended jobs (jobs they haven't applied to)
    applied_job_ids = applications.values_list('job_id', flat=True)
    recommended_jobs = Job.objects.exclude(id__in=applied_job_ids).filter(is_active=True)[:5]

    context = {
        "applications": applications,
        "recommended_jobs": recommended_jobs,
        "total_applications": total_applications,
        "accepted_applications": accepted_applications,
        "rejected_applications": rejected_applications,
    }
    return render(request, "accounts/applicant_dashboard.html", context)

@login_required
def view_profile(request):
    return render(request, "accounts/profile.html")
