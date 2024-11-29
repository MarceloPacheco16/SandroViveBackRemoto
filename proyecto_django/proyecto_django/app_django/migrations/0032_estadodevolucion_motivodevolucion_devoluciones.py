# Generated by Django 5.0.4 on 2024-11-26 07:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_django', '0031_alter_producto_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoDevolucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MotivoDevolucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Devoluciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_solicitud', models.DateField(auto_now=True)),
                ('cantidad', models.IntegerField()),
                ('observacion', models.TextField(blank=True, max_length=200)),
                ('pedido', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_django.pedido')),
                ('estado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_django.estadodevolucion')),
                ('motivo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_django.motivodevolucion')),
            ],
        ),
    ]