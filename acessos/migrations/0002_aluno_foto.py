# Generated by Django 4.2.5 on 2024-07-11 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acessos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='foto',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
