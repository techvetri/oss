# Generated by Django 3.2.3 on 2021-05-29 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_productdetail_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='user_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='ordertransaction',
            name='user_id',
            field=models.BigIntegerField(),
        ),
    ]
