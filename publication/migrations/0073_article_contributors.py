# Generated by Django 4.1.7 on 2023-03-27 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0072_contributor'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='contributors',
            field=models.ManyToManyField(to='publication.contributor'),
        ),
    ]
