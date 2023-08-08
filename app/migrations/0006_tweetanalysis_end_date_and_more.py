# Generated by Django 4.0.2 on 2022-02-25 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_tweetanalysis_fetched_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetanalysis',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='tweetanalysis',
            name='graph_data_available',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='tweetanalysis',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
