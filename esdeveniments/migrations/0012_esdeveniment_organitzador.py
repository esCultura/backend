# Generated by Django 4.1.7 on 2023-04-20 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuaris', '0003_initial'),
        ('esdeveniments', '0011_alter_esdeveniment_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='esdeveniment',
            name='organitzador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='usuaris.organitzador', verbose_name='Organitzador'),
        ),
    ]
