# Generated by Django 3.2.3 on 2021-06-30 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_servicebooking_service_assign_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicebooking',
            name='service_closed_by',
        ),
    ]
