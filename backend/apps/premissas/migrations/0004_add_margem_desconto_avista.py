from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('premissas', '0003_add_deslocamento_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='premissa',
            name='margem_desconto_avista_percentual',
            field=models.DecimalField(decimal_places=2, default=5.0, help_text='Margem para desconto à vista', max_digits=5),
        ),
    ]
