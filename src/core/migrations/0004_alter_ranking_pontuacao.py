# Generated by Django 5.2 on 2025-07-05 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_quizpergunta_resposta"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ranking",
            name="pontuacao",
            field=models.FloatField(default=0),
        ),
    ]
