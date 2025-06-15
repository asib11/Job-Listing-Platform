from django.urls import path, include

from auth.rest.views.register import UserRegisterView

urlpatterns = [
    path("", UserRegisterView.as_view(), name="user-register"),
]
