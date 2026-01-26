# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamentos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orcamento',
            name='margem_lucro_percentual',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='orcamento',
            name='comissao_percentual',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='orcamento',
            name='imposto_percentual',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
