# Generated by Django 4.1.7 on 2023-03-25 18:30

from django.db import migrations, models
import publication.validators


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0063_alter_articleauthor_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='author',
        ),
        migrations.AddField(
            model_name='issue',
            name='author',
            field=models.ManyToManyField(to='publication.author', validators=[publication.validators.validate_unique]),
        ),
    ]
