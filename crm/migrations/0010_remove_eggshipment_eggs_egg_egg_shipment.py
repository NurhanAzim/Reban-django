# Generated by Django 4.2.4 on 2023-08-16 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_remove_egg_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eggshipment',
            name='eggs',
        ),
        migrations.AddField(
            model_name='egg',
            name='egg_shipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.eggshipment'),
        ),
    ]
