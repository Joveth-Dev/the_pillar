# Generated by Django 4.1.7 on 2023-04-01 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0085_reader_sex'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reader',
            options={'ordering': ['user__first_name', 'user__middle_initial', 'user__last_name']},
        ),
    ]