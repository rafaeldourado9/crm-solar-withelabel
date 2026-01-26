from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('premissas', '0002_remove_premissa_lucro_percentual_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='premissa',
            name='cidade_empresa',
            field=models.CharField(default='Dourados, MS', help_text='Cidade sede da empresa', max_length=200),
        ),
        migrations.AddField(
            model_name='premissa',
            name='consumo_veiculo_km_por_litro',
            field=models.DecimalField(decimal_places=2, default=8.0, help_text='Km por litro', max_digits=5),
        ),
        migrations.AddField(
            model_name='premissa',
            name='preco_combustivel_litro',
            field=models.DecimalField(decimal_places=2, default=6.5, help_text='R$ por litro', max_digits=6),
        ),
        migrations.AddField(
            model_name='premissa',
            name='margem_deslocamento_percentual',
            field=models.DecimalField(decimal_places=2, default=20.0, help_text='Margem sobre custo real', max_digits=5),
        ),
        migrations.AddField(
            model_name='premissa',
            name='cidades_sem_cobranca',
            field=models.JSONField(default=list, help_text="Ex: ['Dourados', 'Itaporã', 'Fátima do Sul']"),
        ),
    ]
