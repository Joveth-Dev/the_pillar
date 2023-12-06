# Generated by Django 4.1.5 on 2023-03-25 10:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publication', '0053_rename_authors_article_author'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Member',
            new_name='Author',
        ),
        migrations.RenameModel(
            old_name='MemberPosition',
            new_name='AuthorPosition',
        ),
    ]
