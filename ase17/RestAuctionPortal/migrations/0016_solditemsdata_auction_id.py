# Generated by Django 2.1.2 on 2018-12-12 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Auctions', '0011_auto_20181118_1644'),
        ('RestAuctionPortal', '0015_remove_test_next_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='solditemsdata',
            name='auction_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Auctions.Auction'),
            preserve_default=False,
        ),
    ]
