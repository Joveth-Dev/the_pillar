# Generated by Django 4.1.7 on 2023-04-01 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0082_remove_issue_end_date_remove_issue_is_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
