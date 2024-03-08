# Generated by Django 4.1.7 on 2024-03-08 19:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_roles'),
        ('training', '0016_alter_certificationstatus_due_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.role'),
        ),
        migrations.AlterField(
            model_name='certificationstatus',
            name='due_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 3, 23, 19, 24, 13, 468278, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='certificationstatus',
            name='scheduled_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 3, 23, 19, 24, 13, 467751, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
