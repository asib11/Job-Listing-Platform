from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsRecruiter
from job.models import Job
from job.rest.serializers.job import JobSerializer, JobListSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
  
            if not self.request.user.is_staff and self.request.user.role != 'RECRUITER':
                queryset = queryset.filter(status='PUBLISHED')
        elif self.action in ['update', 'partial_update', 'destroy']:
            queryset = queryset.filter(recruiter=self.request.user)
        return queryset

    def get_permissions(self):

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsRecruiter]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):

        if self.action == 'list':
            return JobListSerializer
        return JobSerializer

    def perform_create(self, serializer):

        serializer.save(recruiter=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, uid=None):

        job = self.get_object()
        if job.recruiter != request.user:
            return Response(
                {"error": "You don't have permission to publish this job"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        job.status = 'PUBLISHED'
        job.save()
        serializer = self.get_serializer(job)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def close(self, request, uid=None):

        job = self.get_object()
        if job.recruiter != request.user:
            return Response(
                {"error": "You don't have permission to close this job"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        job.status = 'CLOSED'
        job.save()
        serializer = self.get_serializer(job)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def archive(self, request, uid=None):

        job = self.get_object()
        if job.recruiter != request.user:
            return Response(
                {"error": "You don't have permission to archive this job"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        job.status = 'ARCHIVED'
        job.save()
        serializer = self.get_serializer(job)
        return Response(serializer.data)
