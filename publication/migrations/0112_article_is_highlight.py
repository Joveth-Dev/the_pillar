# Generated by Django 4.1.7 on 2023-04-15 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0111_alter_article_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_highlight',
            field=models.BooleanField(default=False),
        ),
    ]