# Generated by Django 5.0.7 on 2024-07-17 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0002_boleto_link_pagamento_boleto_qr_code_pix'),
    ]

    operations = [
        migrations.AddField(
            model_name='boleto',
            name='chave_pix',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
