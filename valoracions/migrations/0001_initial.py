# Generated by Django 4.1.7 on 2023-05-16 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuaris', '0005_alter_perfil_imatge'),
        ('esdeveniments', '0013_esdeveniment_reports'),
    ]

    operations = [
        migrations.CreateModel(
            name='Valoracio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Identidicador')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data creació')),
                ('text', models.CharField(max_length=10000, verbose_name='Text')),
                ('puntuacio', models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='valoracions', to='usuaris.perfil', verbose_name='Creador')),
                ('esdeveniment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='valoracions', to='esdeveniments.esdeveniment', verbose_name='Esdeveniment')),
            ],
        ),
    ]
