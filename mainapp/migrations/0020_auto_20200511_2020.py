# Generated by Django 2.2.6 on 2020-05-11 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_auto_20200511_0240'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='propertyentry',
            options={'ordering': ['-updated_at'], 'verbose_name_plural': 'Property Entries'},
        ),
        migrations.AlterModelOptions(
            name='request',
            options={'ordering': ['-updated_at']},
        ),
    ]
