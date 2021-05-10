# Generated by Django 3.2 on 2021-05-09 23:35

from django.conf import settings
from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0013_alter_card_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='image',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='owner',
            field=models.ForeignKey(default='', on_delete=models.SET(home.models.get_sentinel_user), to='auth.user'),
            preserve_default=False,
        ),
    ]