# Generated by Django 4.1.5 on 2023-08-19 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0020_remove_producto_tipo_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='concepmovimiento',
            name='salida_bienes',
            field=models.CharField(blank=True, choices=[('BMS', 'Bienes Muebles'), ('MTC', 'Materiales de Consumo'), ('AMB', 'Ambos!')], max_length=6, null=True, verbose_name='Bienes que Despacha'),
        ),
    ]