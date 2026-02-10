# Generated migration

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AgenteIA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_agente', models.CharField(default='Solar Bot', max_length=100)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('vendedor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agente_ia', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Agente IA',
                'verbose_name_plural': 'Agentes IA',
                'db_table': 'agentes_ia',
            },
        ),
        migrations.CreateModel(
            name='ConversaIA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensagem', models.TextField()),
                ('resposta', models.TextField()),
                ('tipo_acao', models.CharField(blank=True, max_length=50, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversas_ia', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Conversa IA',
                'verbose_name_plural': 'Conversas IA',
                'db_table': 'conversas_ia',
                'ordering': ['-criado_em'],
            },
        ),
    ]
