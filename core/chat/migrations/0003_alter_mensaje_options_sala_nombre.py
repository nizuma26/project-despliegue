# Generated by Django 4.1.5 on 2023-09-22 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_mensaje_fecha'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mensaje',
            options={'ordering': ('fecha',)},
        ),
        migrations.AddField(
            model_name='sala',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]