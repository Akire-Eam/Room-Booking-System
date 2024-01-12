# Generated by Django 4.2.2 on 2023-07-26 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_authuser_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='can_approve',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authuser',
            name='can_book',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authuser',
            name='can_manage_equipment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authuser',
            name='can_manage_facilities',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authuser',
            name='can_manage_terms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authuser',
            name='can_remark',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authuser',
            name='can_upload_schedules',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authuser',
            name='can_view_bookings',
            field=models.BooleanField(default=False),
        ),
    ]
