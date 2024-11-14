# Generated by Django 5.0.3 on 2024-11-13 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privatelabel', '0018_order_take_action_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_po',
            field=models.FileField(blank=True, null=True, upload_to='attachments/'),
        ),
        migrations.AddField(
            model_name='order',
            name='official_quote',
            field=models.FileField(blank=True, null=True, upload_to='attachments/'),
        ),
        migrations.AddField(
            model_name='order',
            name='quality_agreement',
            field=models.FileField(blank=True, null=True, upload_to='attachments/'),
        ),
        migrations.AddField(
            model_name='order',
            name='terms_and_conditions',
            field=models.FileField(blank=True, null=True, upload_to='attachments/'),
        ),
    ]
