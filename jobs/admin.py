from django.contrib import admin
from .models import Job

# Register your models here.

class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company_name", "recruiter", "location", "job_type", "is_active", "posted_at")
    list_filter = ("job_type", "is_active", "remote", "posted_at")
    search_fields = ("title", "company_name", "description", "requirements", "location")
    readonly_fields = ("posted_at", "updated_at", "slug")
    ordering = ("-posted_at",)

admin.site.register(Job, JobAdmin)