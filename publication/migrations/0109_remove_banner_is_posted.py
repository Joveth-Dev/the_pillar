# Generated by Django 4.1.7 on 2023-04-11 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0108_alter_banner_article'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='is_posted',
        ),
    ]
