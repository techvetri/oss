# Generated by Django 3.2.3 on 2021-06-30 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicebooking',
            name='service_assign_to',
            field=models.ForeignKey(db_column='employee_name', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.employee'),
        ),
    ]