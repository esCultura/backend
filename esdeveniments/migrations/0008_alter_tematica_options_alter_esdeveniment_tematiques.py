# Generated by Django 4.1.7 on 2023-03-21 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esdeveniments', '0007_alter_esdeveniment_tematiques'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tematica',
            options={'verbose_name_plural': 'Temàtiques'},
        ),
        migrations.AlterField(
            model_name='esdeveniment',
            name='tematiques',
            field=models.ManyToManyField(to='esdeveniments.tematica'),
        ),
    ]