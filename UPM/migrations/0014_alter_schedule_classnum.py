# Generated by Django 4.2.4 on 2023-09-21 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UPM', '0013_schedulefile_datesubmitted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='classnum',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
