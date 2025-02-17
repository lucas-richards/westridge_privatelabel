# Generated by Django 5.0.3 on 2024-10-14 23:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privatelabel', '0016_rename_note_note_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Deposit', 'Deposit'), ('Ingredients', 'Ingredients'), ('Spec', 'Spec'), ('Package', 'Package'), ('Cap', 'Cap'), ('Label', 'Label'), ('Box', 'Box'), ('Schedule', 'Schedule'), ('Ship', 'Ship')], default='Deposit', max_length=20),
        ),
        migrations.AlterField(
            model_name='note',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes', to='privatelabel.order'),
        ),
    ]
