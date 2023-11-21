# Generated by Django 4.1.5 on 2023-11-01 20:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('erp', '0042_remove_categoria_created_remove_categoria_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoria',
            options={'ordering': ['-id'], 'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        ),
        migrations.AlterField(
            model_name='desincalmacen',
            name='estado',
            field=models.CharField(choices=[('EN CREACIÓN', 'En creación'), ('POR APROBAR', 'Por aprobar')], default='EN CREACIÓN', max_length=25),
        ),
        migrations.AlterField(
            model_name='desincproduc',
            name='estado',
            field=models.CharField(choices=[('EN CREACIÓN', 'En creación'), ('POR APROBAR', 'Por aprobar')], default='EN CREACIÓN', max_length=25),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='cod_salida',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='destino',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salidaproduc_destino_set', to='erp.unidad'),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='estado',
            field=models.CharField(choices=[('EN CREACIÓN', 'En creación'), ('POR APROBAR', 'Por aprobar')], default='EN CREACIÓN', max_length=25),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='fecha_salida',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='iva',
            field=models.DecimalField(decimal_places=2, default=0.16, max_digits=14),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='num_comprob',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='observ',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='origen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salidaproduc_almacen_set', to='erp.almacen'),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='respon_destino',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='respon_origen',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='tipo_comprob',
            field=models.CharField(blank=True, choices=[('FAC', 'Factura'), ('NTD', 'Nota debito'), ('NTE', 'Nota entrega'), ('MEM', 'Memorandum')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='tipo_salida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.concepmovimiento'),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='salidaproduc',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salidaproduc_user_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='trasladoproduc',
            name='estado',
            field=models.CharField(choices=[('EN CREACIÓN', 'En creación'), ('POR APROBAR', 'Por aprobar')], default='EN CREACIÓN', max_length=25),
        ),
    ]