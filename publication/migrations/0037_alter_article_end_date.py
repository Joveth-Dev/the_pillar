# Generated by Django 4.1.5 on 2023-03-18 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0036_alter_article_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='end_date',
            field=models.DateField(),
        ),
    ]
