# Generated by Django 4.0.2 on 2022-02-15 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_sentimet_data_tweetanalysis_sentiment_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetanalysis',
            name='hour_data',
            field=models.TextField(null=True),
        ),
    ]