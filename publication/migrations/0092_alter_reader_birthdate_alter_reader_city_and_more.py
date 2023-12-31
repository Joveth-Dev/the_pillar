# Generated by Django 4.1.7 on 2023-04-01 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0091_remove_reader_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reader',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reader',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reader',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
