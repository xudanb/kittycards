# Generated by Django 3.2 on 2021-05-09 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20210509_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='coins_withholded',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='coins',
            field=models.IntegerField(default=1000),
        ),
    ]
