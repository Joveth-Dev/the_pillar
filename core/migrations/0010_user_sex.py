# Generated by Django 4.1.7 on 2023-04-01 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_delete_tryprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Not set')], default='N', max_length=1),
        ),
    ]