# Generated by Django 4.1.5 on 2023-09-07 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0027_alter_ingresoproduc_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, default='producto/img_articulo.png', null=True, upload_to='producto/', verbose_name='Insertar Imagen'),
        ),
    ]