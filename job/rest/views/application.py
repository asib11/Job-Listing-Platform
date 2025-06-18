from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from core.permissions import IsRecruiter, IsCandidate
from job.models import JobApplication, Job
from job.rest.serializers.application import (
    JobApplicationCreateSerializer,
    JobApplicationListSerializer,
    JobApplicationDetailSerializer
)


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.role == 'CANDIDATE':
            return queryset.filter(candidate=user)
        elif user.role == 'RECRUITER':
            return queryset.filter(job__recruiter=user)
        return queryset.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return JobApplicationCreateSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return JobApplicationDetailSerializer
        return JobApplicationListSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsCandidate]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsRecruiter]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)

    @action(detail=True, methods=['post'])
    def change_status(self, request, uid=None):
        application = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'Status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if application.job.recruiter != request.user:
            return Response(
                {'error': 'Not authorized to change this application\'s status'},
                status=status.HTTP_403_FORBIDDEN
            )

        valid_statuses = ['PENDING', 'REVIEWED', 'SHORTLISTED', 'REJECTED', 'ACCEPTED']
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = new_status
        application.save()
        serializer = self.get_serializer(application)
        return Response(serializer.data)
