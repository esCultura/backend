# Generated by Django 4.1.7 on 2023-03-18 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esdeveniments', '0002_rename_event_esdeveniment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esdeveniment',
            name='dataFi',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data fi'),
        ),
        migrations.AlterField(
            model_name='esdeveniment',
            name='dataIni',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data inici'),
        ),
    ]
