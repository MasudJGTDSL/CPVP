# Generated by Django 5.1.4 on 2024-12-16 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nursery', '0002_cpvp'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpvp',
            name='occupation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
