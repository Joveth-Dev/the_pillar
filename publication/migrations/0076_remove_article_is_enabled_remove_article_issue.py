# Generated by Django 4.1.7 on 2023-04-01 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0075_alter_article_authors_alter_article_contributors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='is_enabled',
        ),
        migrations.RemoveField(
            model_name='article',
            name='issue',
        ),
    ]
