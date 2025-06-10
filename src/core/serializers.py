from rest_framework import serializers
from .models import Area, Conteudo, Pergunta, Resposta, Quiz, QuizConteudo, QuizPergunta
from django.contrib.auth import get_user_model


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'nome']


class ConteudoSerializer(serializers.ModelSerializer):
    area = AreaSerializer() 

    class Meta:
        model = Conteudo
        fields = ['id', 'nome', 'area']


class PerguntaSerializer(serializers.ModelSerializer):
    conteudo = ConteudoSerializer()

    class Meta:
        model = Pergunta
        fields = ['id', 'pergunta', 'nivel', 'conteudo']


class RespostaSerializer(serializers.ModelSerializer):
    pergunta = PerguntaSerializer() 

    class Meta:
        model = Resposta
        fields = ['id', 'resposta', 'correta', 'pergunta']


class QuizSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    area = AreaSerializer()
    
    class Meta:
        model = Quiz
        fields = ['id', 'usuario', 'area', 'nivel', 'pontuacao', 'criacao']


class QuizConteudoSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer()
    conteudo = ConteudoSerializer()

    class Meta:
        model = QuizConteudo
        fields = ['id', 'quiz', 'conteudo']


class QuizPerguntaSerializer(serializers.ModelSerializer):
    quiz_conteudo = QuizConteudoSerializer()
    pergunta = PerguntaSerializer()
    resposta = RespostaSerializer()

    class Meta:
        model = QuizPergunta
        fields = ['id', 'quiz_conteudo', 'pergunta', 'resposta']
