# Generated by Django 4.0.2 on 2022-02-25 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_tweetanalysis_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetanalysis',
            name='end_date',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tweetanalysis',
            name='start_date',
            field=models.CharField(max_length=100, null=True),
        ),
    ]