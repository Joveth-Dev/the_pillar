# Generated by Django 4.1.7 on 2023-04-11 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0104_alter_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]