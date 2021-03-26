from django.urls import path, include
from tokenapp.views import (
    TokenAPIView,
)

urlpatterns = [
    path('token', TokenAPIView.as_view()),
]
