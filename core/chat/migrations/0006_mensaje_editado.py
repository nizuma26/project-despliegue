# Generated by Django 4.1.5 on 2023-09-28 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_sala_nombre_alter_sala_tipo_sala'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensaje',
            name='editado',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]