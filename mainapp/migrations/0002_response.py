# Generated by Django 2.2.6 on 2020-04-18 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('response_status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined')], max_length=20)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Request')),
                ('seller_property_entry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.PropertyEntry')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]