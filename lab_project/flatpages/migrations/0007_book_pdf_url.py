# Generated by Django 4.1 on 2024-10-16 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0006_book_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pdf_url',
            field=models.URLField(blank=True, help_text='URL для PDF файла книги', null=True),
        ),
    ]
