# Generated by Django 4.1.7 on 2023-04-01 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0084_reader_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reader',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Not set')], default='N', max_length=1),
        ),
    ]
