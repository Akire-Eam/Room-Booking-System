# Generated by Django 4.2.2 on 2023-07-31 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=25, null=True)),
                ('log', models.CharField(max_length=300, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
