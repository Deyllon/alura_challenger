# Generated by Django 4.0.4 on 2022-05-13 03:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_da_transacao', models.DateField()),
                ('horario_import', models.DateTimeField(default=datetime.datetime(2022, 5, 13, 0, 18, 21, 188778))),
                ('nome_usuario', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banco_emissor', models.TextField(max_length=200)),
                ('agencia_banco_emissor', models.TextField(max_length=10)),
                ('numero_banco_emissor', models.TextField(max_length=20)),
                ('banco_destinatario', models.TextField(max_length=200)),
                ('agencia_banco_destinatario', models.TextField(max_length=10)),
                ('numero_banco_destinatario', models.TextField(max_length=20)),
                ('valor_transacao', models.FloatField()),
                ('dia_da_transacao', models.DateField()),
                ('horario_import', models.DateTimeField(default=datetime.datetime(2022, 5, 13, 0, 18, 21, 189778))),
                ('nome_usuario', models.TextField(max_length=100)),
                ('arquivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenger.arquivo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.usuarios')),
            ],
        ),
    ]
