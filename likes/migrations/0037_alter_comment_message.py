# Generated by Django 4.1.7 on 2023-04-23 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0036_alter_comment_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.TextField(),
        ),
    ]