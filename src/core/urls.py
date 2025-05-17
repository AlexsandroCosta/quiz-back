from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()

router.register(r'informacoes', views.InfoViewSet, basename='informacoes')

urlpatterns = [
    path('', include(router.urls)),
]