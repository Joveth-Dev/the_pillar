# Generated by Django 4.1.7 on 2023-04-08 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0100_rename_announcement_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='update',
            name='announcement_img',
        ),
        migrations.AddField(
            model_name='update',
            name='image',
            field=models.ImageField(default='+', max_length=255, upload_to='update/images'),
            preserve_default=False,
        ),
    ]