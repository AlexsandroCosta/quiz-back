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
    class Meta:
        model = Quiz
        fields = '__all__'

class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranking
        fields = '__all__'