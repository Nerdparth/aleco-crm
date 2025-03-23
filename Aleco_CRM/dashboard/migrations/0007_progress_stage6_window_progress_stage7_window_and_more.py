# Generated by Django 5.1.7 on 2025-03-19 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_inventoryhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='stage6_window',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='progress',
            name='stage7_window',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='progress',
            name='stage8_window',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='progress',
            name='stage9_window',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='projects',
            name='stage6',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='projects',
            name='stage6_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='projects',
            name='stage7',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='projects',
            name='stage7_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='projects',
            name='stage8',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='projects',
            name='stage8_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='projects',
            name='stage9',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='projects',
            name='stage9_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
