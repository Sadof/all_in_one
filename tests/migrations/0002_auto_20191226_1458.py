# Generated by Django 3.0.1 on 2019-12-26 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='test',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]