# Generated by Django 5.0.7 on 2024-07-27 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acessos', '0011_professor_alunos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professor',
            name='alunos',
        ),
    ]
