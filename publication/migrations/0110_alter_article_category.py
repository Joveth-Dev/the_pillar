# Generated by Django 4.1.7 on 2023-04-12 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0109_remove_banner_is_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('N', 'News'), ('NF', 'News Feature'), ('F', 'Feature'), ('O', 'Opinion'), ('C', 'Culture'), ('E', 'Editorial'), ('L', 'Literary'), ('S', 'Sports')], max_length=2),
        ),
    ]
