# Generated by Django 4.0.4 on 2022-05-13 03:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arquivo',
            name='horario_import',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 13, 0, 19, 0, 790276)),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='horario_import',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 13, 0, 19, 0, 790276)),
        ),
    ]
