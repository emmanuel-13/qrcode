# Generated by Django 4.2 on 2024-11-01 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barcode', '0002_alter_certificate_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
    ]