# Generated by Django 4.1.5 on 2023-06-30 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0016_remove_detingresoproduc_fecha_venc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detsalidaprod',
            name='cant',
            field=models.IntegerField(default=1.0, verbose_name='Cantidad'),
        ),
    ]