# Generated by Django 4.0 on 2021-12-27 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0006_alter_message_sender_alter_message_sent_for'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='uid',
        ),
        migrations.AlterField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(related_name='chat', to='chats.Message'),
        ),
    ]