# Generated by Django 4.1.5 on 2023-03-21 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0042_articlecollaborator'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArticleCollaborator',
        ),
    ]
