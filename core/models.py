from django.contrib.auth.models import AbstractUser
from django.db import models
from . validators import validate_image_size


class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    NOT_SET = 'N'
    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NOT_SET, 'Not set'),
    ]
    avatar = models.ImageField(
        upload_to='core/images',
        default='images/default_contributor_avatar.png',
        validators=[validate_image_size])
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_initial = models.CharField(
        max_length=1,
        default='',
        null=True,
        blank=True)
    email = models.EmailField(unique=True)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default=SEX_CHOICES[2][0])

    def get_full_name(self) -> str:
        if self.middle_initial == None:
            return f'{self.first_name} {self.last_name}'
        return f'{self.first_name} {self.middle_initial}. {self.last_name}'

    def __str__(self) -> str:
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if self.middle_initial:
            self.middle_initial = self.middle_initial.upper()
        super(User, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # set is_active to False instead of deleting
        self.is_active = False
        super(User, self).save(*args, **kwargs)
