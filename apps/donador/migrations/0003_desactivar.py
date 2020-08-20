# Generated by Django 2.2.3 on 2020-07-28 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donador', '0002_auto_20200625_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desactivar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.CharField(max_length=10)),
                ('fecha_donacion', models.DateField()),
                ('Donador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donador.Donador')),
            ],
        ),
    ]
