# Generated by Django 5.0.7 on 2024-07-26 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acessos', '0005_professor_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='professores',
            field=models.ManyToManyField(blank=True, related_name='alunos_associados', to='acessos.professor'),
        ),
        migrations.AlterField(
            model_name='professor',
            name='alunos',
            field=models.ManyToManyField(related_name='professores_associados', to='acessos.aluno'),
        ),
    ]
