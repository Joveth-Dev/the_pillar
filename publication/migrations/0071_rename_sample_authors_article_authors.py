# Generated by Django 4.1.7 on 2023-03-25 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0070_delete_articleauthor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='sample_authors',
            new_name='authors',
        ),
    ]
