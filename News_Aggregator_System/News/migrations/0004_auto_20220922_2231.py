# Generated by Django 3.0.5 on 2022-09-22 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0003_userinfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='last_login_data',
            new_name='last_login_date',
        ),
    ]