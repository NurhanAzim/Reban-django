# Generated by Django 4.2.4 on 2023-08-09 04:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_alter_chicken_health_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='chicken',
            name='date_added',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='chicken',
            name='purpose',
            field=models.PositiveIntegerField(choices=[(0, 'Petelur'), (1, 'Pedaging')], default=0),
        ),
        migrations.AlterField(
            model_name='chicken',
            name='health_status',
            field=models.PositiveIntegerField(choices=[(0, 'Sihat'), (1, 'Sakit')]),
        ),
        migrations.AlterField(
            model_name='chicken',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='egg',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='egg',
            name='size',
            field=models.PositiveIntegerField(choices=[(0, 'Kecil'), (1, 'Sederhana'), (2, 'Besar')]),
        ),
    ]
