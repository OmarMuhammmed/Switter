# Generated by Django 5.1 on 2025-01-22 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
