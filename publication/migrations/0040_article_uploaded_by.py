# Generated by Django 4.1.5 on 2023-03-21 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0039_rename_is_approved_issue_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='uploaded_by',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, related_name='article_uploader', to='publication.member'),
            preserve_default=False,
        ),
    ]
