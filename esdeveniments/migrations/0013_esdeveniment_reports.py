# Generated by Django 4.1.7 on 2023-05-03 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esdeveniments', '0012_esdeveniment_organitzador'),
    ]

    operations = [
        migrations.AddField(
            model_name='esdeveniment',
            name='reports',
            field=models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name="Usuaris que han reportat l'esdeveniment"),
        ),
    ]
