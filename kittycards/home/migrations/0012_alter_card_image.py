# Generated by Django 3.2 on 2021-05-09 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_card_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='image',
            field=models.CharField(default='138878.2.jpg', max_length=100),
        ),
    ]