from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsRecruiter
from job.models import Job, JobApplication
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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsRecruiter])
    def dashboard(self, request):
        recruiter = request.user
        
        # Get job statistics
        total_published = Job.objects.filter(
            recruiter=recruiter, 
            status='PUBLISHED'
        ).count()
        
        total_closed = Job.objects.filter(
            recruiter=recruiter, 
            status='CLOSED'
        ).count()

        # Get application statistics
        total_applications = JobApplication.objects.filter(
            job__recruiter=recruiter
        ).count()
        
        total_hired = JobApplication.objects.filter(
            job__recruiter=recruiter,
            status='ACCEPTED'
        ).count()
        
        total_rejected = JobApplication.objects.filter(
            job__recruiter=recruiter,
            status='REJECTED'
        ).count()

        return Response({
            'total_published_jobs': total_published,
            'total_closed_jobs': total_closed,
            'total_applications': total_applications,
            'total_candidates_hired': total_hired,
            'total_candidates_rejected': total_rejected
        })
