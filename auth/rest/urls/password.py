from django.urls import path
from auth.rest.views.password import ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path('forgot/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset/', ResetPasswordView.as_view(), name='reset-password'),
]
