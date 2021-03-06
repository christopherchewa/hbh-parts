# Generated by Django 2.2.6 on 2020-05-13 00:24

from django.db import migrations, models
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0024_auto_20200512_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyentryimage',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to=mainapp.models.upload_location),
        ),
        migrations.AddField(
            model_name='propertyentryimage',
            name='image5',
            field=models.ImageField(blank=True, null=True, upload_to=mainapp.models.upload_location),
        ),
        migrations.AlterField(
            model_name='propertyentryimage',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to=mainapp.models.upload_location),
        ),
        migrations.AlterField(
            model_name='propertyentryimage',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=mainapp.models.upload_location),
        ),
        migrations.AlterField(
            model_name='propertyentryimage',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=mainapp.models.upload_location),
        ),
    ]
