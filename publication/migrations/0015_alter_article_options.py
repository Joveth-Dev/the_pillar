# Generated by Django 4.1.5 on 2023-01-06 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0014_alter_article_options_alter_issue_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'permissions': [('approve', 'Can approve article'), ('disapprove', 'Can disapprove article'), ('enable', 'Can enable article'), ('disable', 'Can disable article')]},
        ),
    ]