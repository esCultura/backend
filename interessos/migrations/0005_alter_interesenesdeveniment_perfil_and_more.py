# Generated by Django 4.1.7 on 2023-04-20 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuaris', '0003_initial'),
        ('interessos', '0004_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interesenesdeveniment',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interessos_esdeveniment', to='usuaris.perfil', verbose_name='Id perfil'),
        ),
        migrations.AlterField(
            model_name='interesentematica',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interessos_tematica', to='usuaris.perfil', verbose_name='Id perfil'),
        ),
    ]
