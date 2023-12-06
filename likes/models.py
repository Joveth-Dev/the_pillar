from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ['article', 'update', 'issue']}
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    is_liked = models.BooleanField(default=True)  # dislike if False

    def __str__(self) -> str:
        if not self.is_liked:
            return 'Dislike'
        return 'Like'

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    # limiting the input to only article models
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ['article', 'update']}
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    message = models.TextField()
    comment_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'ID : {str(self.id)}'


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    message = models.TextField()
    reply_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        message = self.message
        if len(message) > 50:
            message = message[:50]
            return message.rstrip() + '...'
        return message

    def save(self, *args, **kwargs):
        # pop the request parameter from kwargs, default to None
        request = kwargs.pop('request', None)
        if request and request.user.is_authenticated:
            self.user = request.user  # set the user field to the current user from the request
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Replies'
