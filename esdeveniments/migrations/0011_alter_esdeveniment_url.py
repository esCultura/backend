# Generated by Django 4.1.7 on 2023-03-24 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esdeveniments', '0010_alter_esdeveniment_codi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esdeveniment',
            name='url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='URL organitzador'),
        ),
    ]
