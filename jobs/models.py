# jobs/models.py
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator
import uuid

User = settings.AUTH_USER_MODEL

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ("Full-time", "Full-time"),
        ("Part-time", "Part-time"),
        ("Internship", "Internship"),
        ("Contract", "Contract"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recruiter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="jobs"
    )  # expects custom User model with is_recruiter property
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)  # free text
    description = models.TextField()
    requirements = models.TextField(blank=True)
    salary_min = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    salary_max = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default="Full-time")
    remote = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)   # soft-close posting
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=300, blank=True, db_index=True, unique=True)

    class Meta:
        ordering = ["-posted_at"]
        indexes = [
            models.Index(fields=["-posted_at"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.title} @ {self.company_name}"

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        # Generate a unique slug the first time or if title changed and slug empty
        if not self.slug:
            base = slugify(f"{self.title}-{self.company_name}")[:200]
            slug = base
            counter = 1
            while Job.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
