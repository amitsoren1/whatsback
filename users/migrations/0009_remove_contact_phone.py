# Generated by Django 4.0 on 2021-12-26 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_contact_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='phone',
        ),
    ]
