# Generated by Django 3.0.1 on 2020-01-16 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0007_test_users_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
