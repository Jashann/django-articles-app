# Generated by Django 3.2 on 2021-05-15 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='createdAt',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
