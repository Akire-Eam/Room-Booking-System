# Generated by Django 4.2.4 on 2023-09-20 06:49

import UPM.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UPM', '0010_schedule_faculty_emails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedulefile',
            name='file',
        ),
        migrations.AddField(
            model_name='schedulefile',
            name='attachFile',
            field=UPM.models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
