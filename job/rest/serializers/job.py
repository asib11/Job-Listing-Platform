from rest_framework import serializers
from job.models import Job


class JobSerializer(serializers.ModelSerializer):

    recruiter_name = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    job_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'uid',
            'title',
            'description',
            'recruiter',
            'recruiter_name',
            'job_type',
            'job_type_display',
            'location',
            'salary_min',
            'salary_max',
            'deadline',
            'requirements',
            'responsibilities',
            'status',
            'status_display',
            'company_name',
            'company_description',
            'experience_required',
            'skills_required',
            'benefits',
            'is_featured',
            'views_count',
            'applications_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'uid',
            'recruiter',
            'views_count',
            'applications_count',
            'created_at',
            'updated_at'
        ]

    def get_recruiter_name(self, obj):
        return f"{obj.recruiter.first_name} {obj.recruiter.last_name}"

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_job_type_display(self, obj):
        return obj.get_job_type_display()

    def validate(self, data):
        if data.get('salary_min') and data.get('salary_max'):
            if data['salary_min'] > data['salary_max']:
                raise serializers.ValidationError({
                    "salary_min": "Minimum salary cannot be greater than maximum salary"
                })
        return data


class JobListSerializer(JobSerializer):
    class Meta(JobSerializer.Meta):
        fields = [
            'uid',
            'title',
            'company_name',
            'location',
            'job_type',
            'job_type_display',
            'salary_min',
            'salary_max',
            'deadline',
            'status',
            'status_display',
            'is_featured',
            'created_at'
        ]
