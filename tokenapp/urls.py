from django.urls import path, include
from tokenapp.views import (
    TokenAPIView,
    ResourceAPIView,
)

urlpatterns = [
    path('token', TokenAPIView.as_view()),
    path('resource', ResourceAPIView.as_view()),
]
