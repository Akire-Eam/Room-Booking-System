# Generated by Django 4.2.4 on 2023-08-22 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UPM', '0004_remove_schedulefile_ocs_schedulefile_uploader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='semester',
            field=models.CharField(choices=[('1st SEMESTER', '1st Semester'), ('2nd SEMESTER', '2nd Semester'), ('MIDYEAR', 'Midyear')], max_length=50, null=True),
        ),
    ]
