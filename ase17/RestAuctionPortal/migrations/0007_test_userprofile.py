# Generated by Django 2.1.2 on 2018-12-07 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestAuctionPortal', '0006_auto_20181207_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='userprofile',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
