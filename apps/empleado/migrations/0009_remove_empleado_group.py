# Generated by Django 2.2.3 on 2019-10-01 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empleado', '0008_empleado_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empleado',
            name='group',
        ),
    ]