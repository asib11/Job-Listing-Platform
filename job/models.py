from django.db import models
from django.core.validators import MinValueValidator
from core.models import User
from shared.base_model import BaseModel
from job.choices import JobStatusChoices, JobTypeChoices


class Job(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    recruiter = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='posted_jobs',
        limit_choices_to={'role': 'RECRUITER'}
    )
    job_type = models.CharField(
        max_length=20,
        choices=JobTypeChoices.choices,
        default=JobTypeChoices.FULL_TIME
    )
    location = models.CharField(max_length=255)
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    deadline = models.DateTimeField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=JobStatusChoices.choices,
        default=JobStatusChoices.DRAFT
    )
    company_name = models.CharField(max_length=255)
    company_description = models.TextField(blank=True)
    experience_required = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    skills_required = models.TextField()
    benefits = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    applications_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("can_publish_job", "Can publish job"),
            ("can_feature_job", "Can feature job"),
        ]

    def __str__(self):
        return f"{self.title} at {self.company_name}"

    def save(self, *args, **kwargs):
        # Auto-generate unique job ID if not exists
        if not self.uid:
            import uuid
            self.uid = f"JOB-{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)