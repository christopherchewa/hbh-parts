# Generated by Django 2.2.6 on 2020-05-10 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_auto_20200510_0040'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['-updated_at']},
        ),
    ]
