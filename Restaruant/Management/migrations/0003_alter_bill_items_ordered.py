# Generated by Django 3.2.6 on 2021-08-10 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0002_auto_20210810_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='items_ordered',
            field=models.CharField(max_length=255),
        ),
    ]