# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('tipo', models.CharField(choices=[('orcamento', 'Orçamento'), ('contrato', 'Contrato'), ('proposta', 'Proposta')], max_length=20)),
                ('arquivo', models.FileField(upload_to='templates/')),
                ('arquivo_nome', models.CharField(max_length=255)),
                ('ativo', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'templates',
                'ordering': ['-created_at'],
            },
        ),
    ]
