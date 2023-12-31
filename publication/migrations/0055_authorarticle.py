# Generated by Django 4.1.5 on 2023-03-25 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0054_rename_member_author_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='publication.article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publication.author')),
            ],
        ),
    ]
