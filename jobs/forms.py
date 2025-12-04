# jobs/forms.py
from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "company_name",
            "location",
            "description",
            "requirements",
            "salary_min",
            "salary_max",
            "job_type",
            "remote",
            "is_active",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "requirements": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned = super().clean()
        smin = cleaned.get("salary_min")
        smax = cleaned.get("salary_max")
        if smin and smax and smin > smax:
            raise forms.ValidationError("Minimum salary cannot be greater than maximum salary.")
        return cleaned
