# Generated by Django 2.1.2 on 2018-12-08 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RestAuctionPortal', '0008_test_auctionid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='userprofile',
            field=models.ForeignKey(default='adiProfile', on_delete=django.db.models.deletion.DO_NOTHING, to='Users.Profile'),
        ),
    ]
