from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        post_migrate.connect(povoar_db, sender=self)


def povoar_db(sender, **kwargs):
    from .models import Area, Conteudo, Pergunta, Resposta
    from .utils.areas_conteudos import data

    if not Area.objects.all().exists():
        for area, conteudos in data.items():
            area_obj = Area.objects.create(nome=area)

            for conteudo, dados in conteudos.items():
                conteudo_obj = Conteudo.objects.create(area=area_obj, nome=conteudo)

                for obj in dados:
                    pergunta_obj = Pergunta.objects.create(
                        conteudo=conteudo_obj,
                        pergunta=obj["pergunta"],
                        nivel=obj["nivel"],
                    )

                    for resposta, correta in obj["respostas"].items():
                        Resposta.objects.create(
                            pergunta=pergunta_obj, resposta=resposta, correta=correta
                        )
