# Generated by Django 2.2.3 on 2019-11-06 03:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospital', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_nacimiento', models.DateField()),
                ('direccion', models.CharField(max_length=50)),
                ('genero', models.CharField(choices=[('M', 'masculino'), ('F', 'femenino')], default='M', max_length=1)),
                ('grupo_sanguineo', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('0', '0')], default='A', max_length=10)),
                ('factor_sanguineo', models.CharField(choices=[('+', 'positivo'), ('-', 'negativo')], default='+', max_length=2)),
                ('telefono', models.CharField(max_length=12)),
                ('activo', models.BooleanField(default=0)),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.Hospital')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
