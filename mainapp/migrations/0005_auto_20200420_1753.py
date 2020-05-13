# Generated by Django 2.2.6 on 2020-04-20 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20200419_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='request_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Matched', 'Matched'), ('Inactive', 'Inactive')], default='Pending', max_length=20),
        ),
    ]