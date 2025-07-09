from rest_framework import serializers
from .models import (
    Area, 
    Conteudo,
    Quiz,
    Ranking
)

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class ConteudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conteudo
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    area_nome = serializers.CharField(source='area.nome', read_only=True)
    nivel_display = serializers.CharField(source='get_nivel_display', read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'usuario', 'area', 'area_nome', 'nivel', 'nivel_display', 'pontuacao', 'criacao']

class RankingSerializer(serializers.ModelSerializer):
    nome_usuario = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Ranking
        fields =['id', 'usuario', 'nome_usuario', 'pontuacao']