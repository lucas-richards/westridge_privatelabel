# Generated by Django 5.0.3 on 2025-01-31 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privatelabel', '0028_alter_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='coordinator_notes',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='planning_notes',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
