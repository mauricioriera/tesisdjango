# Generated by Django 2.2.3 on 2019-09-28 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('empleado', '0002_auto_20190824_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
