# Generated by Django 5.0.4 on 2024-11-26 08:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_django', '0032_estadodevolucion_motivodevolucion_devoluciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='devoluciones',
            name='producto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_django.producto'),
        ),
    ]