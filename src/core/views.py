from django.shortcuts import render
from rest_framework import permissions, viewsets, authentication
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from .models import (
    Area,
    Conteudo
)
from .serializers import (
    AreaSerializer,
    ConteudoSerializer
)

class InfoViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        tags=['Informações'],
        operation_description='Lista todas áreas de conhecimento registrada',
        responses={
            200: AreaSerializer(many=True)
        }
    )
    @action(detail=False, url_path='area')
    def area(self, request):
        areas = Area.objects.all()
        serializer = AreaSerializer(areas, many=True)

        return Response(serializer.data, status=200)
    
    @swagger_auto_schema(
        tags=['Informações'],
        operation_description='Lista todos conteúdos de uma area de conhecimento',
        responses={
            200: AreaSerializer(many=True)
        }
    )
    @action(detail=False, url_path='(?P<id_area>[^/.]+)?/conteudo')
    def conteudo(self, request, id_area=None):
        try:
            area = Area.objects.get(id=id_area)
            conteudos = Conteudo.objects.filter(area=area)
            serializer = AreaSerializer(conteudos, many=True)

            return Response(serializer.data, status=200)
        
        except Area.DoesNotExist:
            return Response('Área não encontrada', status=404)
    
