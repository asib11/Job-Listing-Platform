from rest_framework import serializers
from django.utils import timezone
from job.models import JobApplication, Job


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            'job',
            'cover_letter',
            'resume',
            'expected_salary'
        ]

    def validate_job(self, job):
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError('Authentication required.')

        # Check if job exists and is published
        if job.status != 'PUBLISHED':
            raise serializers.ValidationError('Cannot apply to unpublished job.')

        # Check if deadline has passed
        if job.deadline < timezone.now():
            raise serializers.ValidationError('Job application deadline has passed.')

        # Check if user has already applied
        if JobApplication.objects.filter(job=job, candidate=request.user).exists():
            raise serializers.ValidationError('You have already applied to this job.')

        return job

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['candidate'] = request.user
        return super().create(validated_data)


class JobApplicationListSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SerializerMethodField()
    job_title = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = [
            'uid',
            'job',
            'job_title',
            'candidate',
            'candidate_name',
            'status',
            'status_display',
            'expected_salary',
            'created_at'
        ]

    def get_candidate_name(self, obj):
        return f"{obj.candidate.first_name} {obj.candidate.last_name}"

    def get_job_title(self, obj):
        return obj.job.title

    def get_status_display(self, obj):
        return obj.get_status_display()


class JobApplicationDetailSerializer(JobApplicationListSerializer):
    class Meta(JobApplicationListSerializer.Meta):
        fields = JobApplicationListSerializer.Meta.fields + [
            'cover_letter',
            'resume',
            'updated_at'
        ]
