# Generated by Django 4.1.7 on 2023-04-23 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0037_alter_comment_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='message',
            field=models.TextField(),
        ),
    ]
