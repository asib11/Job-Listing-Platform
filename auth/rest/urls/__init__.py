from django.urls import path, include


urlpatterns = [
    path("/register", include("auth.rest.urls.register")),
    path("/token", include("auth.rest.urls.token")),
]