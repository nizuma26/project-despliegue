# Generated by Django 4.1.5 on 2023-09-07 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0028_alter_producto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, default='producto/sin_imagen_2.png', null=True, upload_to='producto/', verbose_name='Insertar Imagen'),
        ),
    ]
