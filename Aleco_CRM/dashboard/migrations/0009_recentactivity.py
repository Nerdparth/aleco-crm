# Generated by Django 5.0.6 on 2025-03-23 19:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_maintenancemode'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(choices=[('measurement', 'measurement'), ('cutting frames', 'cutting frames'), ('cutting sashes', 'cutting sashes'), ('jalli palle', 'jalli palle'), ('assembled', 'assembled '), ('packed', 'packed'), ('beading', 'beading'), ('delivered', 'delivered'), ('installation', 'installation'), ('inventory', 'inventory'), ('ordered', 'ordered')], max_length=250)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.projects')),
            ],
        ),
    ]
