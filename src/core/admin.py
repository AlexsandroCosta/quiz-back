from django.contrib import admin
from .models import Area, Conteudo, Pergunta, Resposta, Quiz, QuizConteudo, QuizPergunta

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

@admin.register(Conteudo)
class ConteudoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'area']
    list_filter = ['area']
    search_fields = ['nome']

@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ['pergunta', 'conteudo', 'nivel']
    list_filter = ['nivel', 'conteudo__area']
    search_fields = ['pergunta']

@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ['resposta', 'pergunta', 'correta']
    list_filter = ['correta']
    search_fields = ['resposta']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'area', 'nivel', 'pontuacao', 'criacao']
    list_filter = ['nivel', 'area']
    search_fields = ['usuario__username']

@admin.register(QuizConteudo)
class QuizConteudoAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'conteudo']
    list_filter = ['conteudo__area']

@admin.register(QuizPergunta)
class QuizPerguntaAdmin(admin.ModelAdmin):
    list_display = ['quiz_conteudo', 'pergunta', 'resposta']