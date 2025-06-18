from django.urls import path, include
from rest_framework.routers import DefaultRouter
from job.rest.views.job import JobViewSet
from job.rest.views.application import JobApplicationViewSet

router = DefaultRouter()
router.register('jobs', JobViewSet, basename='job')
router.register('applications', JobApplicationViewSet, basename='job-application')

urlpatterns = [
    path('', include(router.urls)),
]
