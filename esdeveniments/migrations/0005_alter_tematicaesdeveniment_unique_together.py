# Generated by Django 4.1.7 on 2023-03-19 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('esdeveniments', '0004_tematica_esdeveniment_comarca_esdeveniment_email_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tematicaesdeveniment',
            unique_together={('esdeveniment', 'tematica')},
        ),
    ]
