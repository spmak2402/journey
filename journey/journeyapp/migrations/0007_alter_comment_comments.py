# Generated by Django 5.0.7 on 2024-08-10 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journeyapp', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comments',
            field=models.CharField(default='comment here', max_length=800),
        ),
    ]
