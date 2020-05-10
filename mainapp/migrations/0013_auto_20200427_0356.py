# Generated by Django 2.2.6 on 2020-04-27 00:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_auto_20200427_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyentry',
            name='favourites',
            field=models.ManyToManyField(blank=True, related_name='favourites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Favourite',
        ),
    ]
