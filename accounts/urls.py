# accounts/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name="logout"),
    path("profile/", views.view_profile, name="view_profile"),


    path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path("applicant/dashboard/", views.applicant_dashboard, name="applicant_dashboard"),

]
