from django.urls import path
from .views import DashboardView, PredictionAPIView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('api/predict/', PredictionAPIView.as_view(), name='predict_api'),
]
