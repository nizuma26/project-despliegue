# Generated by Django 4.1.5 on 2023-09-01 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0025_alter_codbienes_procedencia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Código'),
        ),
    ]
