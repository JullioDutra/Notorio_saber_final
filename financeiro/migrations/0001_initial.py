# Generated by Django 4.2.5 on 2024-07-11 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('acessos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boleto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes_referencia', models.DateField()),
                ('arquivo', models.FileField(upload_to='boletos/')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pago', models.BooleanField(default=False)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boletos', to='acessos.aluno')),
            ],
        ),
        migrations.CreateModel(
            name='ComprovantePagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_envio', models.DateTimeField(auto_now_add=True)),
                ('arquivo', models.FileField(upload_to='comprovantes/')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comprovantes', to='acessos.aluno')),
                ('boleto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comprovantes', to='financeiro.boleto')),
            ],
        ),
    ]
