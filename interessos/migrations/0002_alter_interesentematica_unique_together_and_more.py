# Generated by Django 4.1.7 on 2023-04-15 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interessos', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='interesentematica',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='interesentematica',
            name='perfil',
        ),
        migrations.RemoveField(
            model_name='interesentematica',
            name='tematica',
        ),
        migrations.DeleteModel(
            name='InteresEnEsdeveniment',
        ),
        migrations.DeleteModel(
            name='InteresEnTematica',
        ),
    ]
