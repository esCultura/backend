# Generated by Django 4.1.7 on 2023-03-21 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('esdeveniments', '0007_alter_esdeveniment_tematiques'),
        ('usuaris', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InteresEnTematica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuaris.perfil', verbose_name='Username perfil')),
                ('tematica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='esdeveniments.tematica', verbose_name='Nom tematica')),
            ],
            options={
                'unique_together': {('perfil', 'tematica')},
            },
        ),
        migrations.CreateModel(
            name='InteresEnEsdeveniment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esdeveniment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='esdeveniments.esdeveniment', verbose_name='Codi esdeveniment')),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuaris.perfil', verbose_name='Username perfil')),
            ],
            options={
                'unique_together': {('perfil', 'esdeveniment')},
            },
        ),
    ]
