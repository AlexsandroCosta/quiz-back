# Generated by Django 5.2 on 2025-07-09 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_foto"),
    ]

    operations = [
        migrations.AlterField(
            model_name="foto",
            name="foto",
            field=models.ImageField(blank=True, null=True, upload_to="fotos/"),
        ),
    ]
