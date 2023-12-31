# Generated by Django 4.1.7 on 2023-04-11 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0101_remove_update_announcement_img_update_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='date_posted',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='update',
            name='description',
            field=models.TextField(default='+'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='update',
            name='title',
            field=models.CharField(default='+', max_length=255),
            preserve_default=False,
        ),
    ]
