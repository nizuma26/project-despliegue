# Generated by Django 4.1.5 on 2023-10-09 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0037_remove_codbienes_created_remove_codbienes_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departamento',
            name='created',
        ),
        migrations.RemoveField(
            model_name='departamento',
            name='updated',
        ),
    ]
