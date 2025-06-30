from django.db import models
from django.contrib.auth import get_user_model

class Area(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "Áreas"

    def __str__(self):
        return self.nome
    
class Conteudo(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    nome = models.CharField(max_length=70)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['area', 'nome'], name='unique_area_nome')
        ]
        verbose_name = "Conteúdo"
        verbose_name_plural = "Conteúdos"

    def __str__(self):
        return self.nome
    
class Pergunta(models.Model):
    NIVEL_CHOICES = [
        ('facil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil')
    ]

    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE)
    pergunta = models.TextField()
    nivel = models.CharField(max_length=7, choices=NIVEL_CHOICES)

    class Meta:
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return self.pergunta

class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    resposta = models.CharField(max_length=50)
    correta = models.BooleanField()

    class Meta:
        verbose_name_plural = "Respostas"

    def __str__(self):
        return self.resposta

class Quiz(models.Model):
    NIVEL_CHOICES = [
        ('facil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil')
    ]

    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    nivel = models.CharField(max_length=7, choices=NIVEL_CHOICES)
    pontuacao = models.FloatField(default=0)
    criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"Quiz de {self.usuario} ({self.area.nome} - {self.nivel})"

class QuizConteudo(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['quiz', 'conteudo'], name='unique_quiz_conteudo')
        ]
        verbose_name = "Conteúdo do Quiz"
        verbose_name_plural = "Conteúdos do Quiz"

class QuizPergunta(models.Model):
    quiz_conteudo = models.ForeignKey(QuizConteudo, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    resposta = models.ForeignKey(Resposta, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['quiz_conteudo', 'pergunta'], name='unique_quiz_pergunta')
        ]
        verbose_name = "Pergunta do Quiz"
        verbose_name_plural = "Perguntas do Quiz"

class Ranking(models.Model):
    usuario = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    pontuacao = models.FloatField(default=0)

    class Meta:
        ordering = ['-pontuacao']
        verbose_name = 'Ranking'
        verbose_name_plural = 'Rankings'

    def __str__(self):
        return f"{self.usuario.username} - {self.pontuacao} pontos"
