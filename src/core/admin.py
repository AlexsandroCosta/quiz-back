from django.contrib import admin
from .models import (
    Area,
    Conteudo,
    Pergunta,
    Resposta,
    Quiz,
    QuizConteudo,
    QuizPergunta,
    Ranking
)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']


@admin.register(Conteudo)
class ConteudoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'area']
    list_filter = ['area']
    search_fields = ['nome']


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ['id', 'pergunta', 'nivel', 'conteudo']
    list_filter = ['nivel', 'conteudo']
    search_fields = ['pergunta']


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ['id', 'resposta', 'correta', 'pergunta']
    list_filter = ['correta']
    search_fields = ['resposta']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'area', 'nivel', 'pontuacao', 'criacao']
    list_filter = ['nivel', 'area']
    search_fields = ['usuario__username']


@admin.register(QuizConteudo)
class QuizConteudoAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz', 'conteudo']
    list_filter = ['conteudo']


@admin.register(QuizPergunta)
class QuizPerguntaAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz_conteudo', 'pergunta', 'resposta']
    search_fields = ['pergunta__pergunta']


@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'pontuacao']
    search_fields = ['usuario__username']
    ordering = ['-pontuacao']
