# Generated by Django 5.0.3 on 2025-01-28 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privatelabel', '0023_alter_component_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customerid',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='Open', max_length=20),
        ),
    ]
