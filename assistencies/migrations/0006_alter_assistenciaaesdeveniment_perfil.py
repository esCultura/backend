# Generated by Django 4.1.7 on 2023-04-20 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuaris', '0003_initial'),
        ('assistencies', '0005_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistenciaaesdeveniment',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assistencies', to='usuaris.perfil', verbose_name='Id perfil'),
        ),
    ]
