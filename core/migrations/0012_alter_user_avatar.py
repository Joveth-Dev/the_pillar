# Generated by Django 4.2.3 on 2023-07-11 05:38

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='images/default_contributor_avatar.png', upload_to='core/images', validators=[core.validators.validate_image_size]),
        ),
    ]
