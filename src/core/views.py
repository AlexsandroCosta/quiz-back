from django.shortcuts import render
from rest_framework import permissions, viewsets, authentication
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import (
    Area,
    Conteudo,
    Quiz,
    Ranking
)
from .serializers import (
    AreaSerializer,
    ConteudoSerializer,
    QuizSerializer,
    RankingSerializer
)

class InfoViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

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
            serializer = ConteudoSerializer(conteudos, many=True)

            return Response(serializer.data, status=200)
        
        except Area.DoesNotExist:
            return Response('Área não encontrada', status=404)
    
    @swagger_auto_schema(
        tags=['Informações'],
        operation_description='Lista o ranking de usuários ordenado pela pontuação total.',
        responses={
            200: RankingSerializer(many=True)
        }
    )
    @action(detail=False, url_path='ranking')
    def ranking(self, request):
        ranking = Ranking.objects.all().order_by('pontuacao')
        serializer = RankingSerializer(ranking, many=True)

        return Response(serializer.data, status=200)

class QuizViewSet(viewsets.ViewSet):
    
    @swagger_auto_schema(
        tags=['Quiz'],
        operation_description='',
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            "nivel" : openapi.Schema(type=openapi.TYPE_STRING, enum=['facil', 'medio', 'dificil']),
            "area" : openapi.Schema(type=openapi.TYPE_INTEGER),
            "conteudos" : openapi.Schema(type=openapi.TYPE_ARRAY, items=
                                         openapi.Schema(type=openapi.TYPE_INTEGER))
        }),
        responses={
            200: QuizSerializer(many=True)
        }
    )
    def create(self, request):
        data = request.data.copy()

        conteudos = Conteudo.objects.filter(id__in=data['conteudos'])
        
        if len(conteudos) != len(data['conteudos']):
            return Response({'detail': 'Um ou mais conteúdos são inválidos.'}, status=400)
        
        data['usuario'] = request.user.id

        serializer = QuizSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response('ok', status=200)
        
        return Response(serializer.errors, status=400)