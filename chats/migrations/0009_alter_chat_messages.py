# Generated by Django 4.0 on 2021-12-27 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0008_alter_chat_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(blank=True, related_name='chat', to='chats.Message'),
        ),
    ]