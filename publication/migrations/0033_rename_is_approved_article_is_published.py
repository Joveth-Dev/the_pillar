# Generated by Django 4.1.5 on 2023-03-18 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0032_remove_banner_try_lng'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='is_approved',
            new_name='is_published',
        ),
    ]
