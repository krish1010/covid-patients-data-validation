# Generated by Django 3.0.7 on 2020-06-10 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validate_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.IntegerField(default=-1),
        ),
    ]
