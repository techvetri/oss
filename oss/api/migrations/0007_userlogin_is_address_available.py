# Generated by Django 3.2.3 on 2021-05-30 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_userdetails_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlogin',
            name='is_address_available',
            field=models.BooleanField(default=False),
        ),
    ]