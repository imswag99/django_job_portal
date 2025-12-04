from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    APPLICANT = "applicant"
    RECRUITER = "recruiter"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (APPLICANT, "Applicant"),
        (RECRUITER, "Recruiter"),
        (ADMIN, "Admin"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=APPLICANT)

    @property
    def is_applicant(self):
        return self.role == self.APPLICANT

    @property
    def is_recruiter(self):
        return self.role == self.RECRUITER

    @property
    def is_admin(self):
        # If user is superuser, always considered admin
        return self.is_superuser or self.role == self.ADMIN

    def save(self, *args, **kwargs):
        # Ensure superusers always have role="admin"
        if self.is_superuser:
            self.role = self.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
