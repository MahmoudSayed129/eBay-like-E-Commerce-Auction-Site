# Generated by Django 3.2.7 on 2021-09-21 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_active_list_closed_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='auction_id',
            field=models.IntegerField(default='0'),
        ),
    ]
