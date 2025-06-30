from rest_framework import serializers
from .models import (
    Area, 
    Conteudo,
    Quiz,
    Ranking
)
from django.contrib.auth import get_user_model

User = get_user_model()

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
    nome = serializers.SerializerMethodField()

    class Meta:
        model = Ranking
        fields = ['usuario', 'nome', 'pontuacao']

    def get_nome(self, obj):
        return obj.usuario.first_name or obj.usuario.username
