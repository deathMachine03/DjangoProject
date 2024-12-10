# Generated by Django 4.1 on 2024-10-15 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='articles/'),
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
