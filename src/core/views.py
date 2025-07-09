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
    Ranking,
    QuizConteudo,
    Pergunta,
    QuizPergunta,
    Resposta
)
from .serializers import (
    AreaSerializer,
    ConteudoSerializer,
    QuizSerializer,
    RankingSerializer
)
from django.db import transaction

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
            try:
                with transaction.atomic():
                    quiz = serializer.save()

                    data = {
                        **serializer.data,
                        'conteudos': []
                    }

                    for conteudo in conteudos:
                        quizConteudo = QuizConteudo.objects.create(
                            quiz = quiz,
                            conteudo = conteudo
                        )

                        perguntas = Pergunta.objects.filter(
                            nivel=quiz.nivel,
                            conteudo=conteudo
                        ).order_by('?')[:int(10/len(conteudos))]

                        data_perguntas = []

                        for pergunta in perguntas:
                            data_respostas = [] 

                            quizPergunta = QuizPergunta.objects.create(
                                quiz_conteudo = quizConteudo,
                                pergunta = pergunta
                            )

                            resposta = Resposta.objects.filter(pergunta=pergunta, correta=True).first()
                            respostas_incorretas = Resposta.objects.filter(pergunta=pergunta, correta=False).order_by('?')[:3]

                            data_respostas.append({
                                'id': resposta.id,
                                'resposta': resposta.resposta,
                                'correta': resposta.correta
                            })

                            for incorreta in respostas_incorretas:
                                data_respostas.append({
                                    'id': incorreta.id,
                                    'resposta': incorreta.resposta,
                                    'correta': incorreta.correta
                                })

                            data_perguntas.append({
                                'quizPergunta_id': quizPergunta.id,
                                'pergunta': pergunta.pergunta,
                                'respostas': data_respostas
                            })

                        data['conteudos'].append({
                            'quizConteudo_id': quizConteudo.id,
                            'conteudo_nome': conteudo.nome,
                            'perguntas': data_perguntas
                        })

                return Response(data, status=201)
            
            except Exception as e:
               return Response({'detail': f'Erro ao criar o quiz: {str(e)}'}, status=500)
        
        return Response(serializer.errors, status=400)
    
    @swagger_auto_schema(
        tags=['Quiz'],
        operation_description='',
        request_body=openapi.Schema(type=openapi.TYPE_ARRAY, items=
                                    openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                        'id_pergunta': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'id_resposta': openapi.Schema(type=openapi.TYPE_INTEGER)
                                    })),
        responses={200: 'ok'}
    )
    def update(self, request, pk):
        try:
            quiz = Quiz.objects.get(id=pk, usuario=request.user)
            pontuacao = 0

            match quiz.nivel:
                case 'facil':
                    ponto = 1
                case 'medio':
                    ponto = 2
                case 'dificil':
                    ponto = 3

            perguntas = QuizPergunta.objects.filter(quiz_conteudo__quiz=quiz)
            data = request.data.copy()
            
            for pergunta in perguntas:
                for obj in data:
                    if obj['id_pergunta'] == pergunta.id:
                        try:
                            resposta = Resposta.objects.get(id=obj['id_resposta'], pergunta=pergunta.pergunta)
                            pergunta.resposta = resposta
                            pergunta.save()

                            if resposta.correta:
                                pontuacao += ponto
                            else:
                                pontuacao -= ponto

                        except Resposta.DoesNotExist:
                            pass
                        
                        data.remove(obj)
                        break

            quiz.pontuacao = pontuacao
            quiz.save()

            ranking, _ = Ranking.objects.get_or_create(usuario=request.user)
            ranking.pontuacao += pontuacao
            ranking.save()

            return Response({'id': pk}, status=200)
        
        except Quiz.DoesNotExist:
            return Response({'detail': 'Quiz não encontrado.'}, status=404)

    @swagger_auto_schema(
            tags=['Quiz'],
            operation_description='Retorna a lista de quizes que o usuario gerou.',
            responses={200: QuizSerializer(many=True)}
    )
    @action(detail=False, url_path='historico')
    def historico(self, request):
        quizes = Quiz.objects.filter(usuario=request.user).order_by('-criacao')

        serializer = QuizSerializer(quizes, many=True)

        return Response(serializer.data, status=200)