from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r"informacoes", views.InfoViewSet, basename="informacoes")
router.register(r"quiz", views.QuizViewSet, basename="quiz")
router.register(r"perfil", views.Perfil, basename="perfil")

urlpatterns = [
    path("", include(router.urls)),
]
