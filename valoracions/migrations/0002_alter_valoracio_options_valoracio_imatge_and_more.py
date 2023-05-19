# Generated by Django 4.1.7 on 2023-05-18 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valoracions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='valoracio',
            options={'verbose_name_plural': 'Valoracions'},
        ),
        migrations.AddField(
            model_name='valoracio',
            name='imatge',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Imatge'),
        ),
        migrations.AlterField(
            model_name='valoracio',
            name='puntuacio',
            field=models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Puntuació'),
        ),
    ]