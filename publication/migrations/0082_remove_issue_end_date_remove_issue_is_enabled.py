# Generated by Django 4.1.7 on 2023-04-01 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0081_alter_article_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='is_enabled',
        ),
    ]
