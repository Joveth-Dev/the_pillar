# Generated by Django 4.1.3 on 2022-11-20 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0002_alter_article_member_alter_issue_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberposition',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='publication.member'),
        ),
    ]
