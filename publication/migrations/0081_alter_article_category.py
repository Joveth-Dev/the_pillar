# Generated by Django 4.1.7 on 2023-04-01 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0080_alter_article_category_alter_article_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('N', 'News'), ('NF', 'News Feature'), ('F', 'Feature'), ('O', 'Opinion'), ('C', 'Culture'), ('E', 'Editorial'), ('L', 'Literary'), ('CT', 'Caption Type')], max_length=2),
        ),
    ]