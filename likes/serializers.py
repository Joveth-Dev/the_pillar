from django.conf import settings
from datetime import datetime
from rest_framework import serializers
from . import models

from django.forms.widgets import Widget


class CustomRepliesWidget(Widget):
    template_name = 'custom_replies_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['replies'] = value
        return context

    def value_from_datadict(self, data, files, name):
        replies_data = data.getlist(f'{name}_replies')
        replies = []

        for reply_data in replies_data:
            reply_dict = dict(item.split('=')
                              for item in reply_data.split('&'))
            reply_serializer = ReplySerializer(data=reply_dict)

            if reply_serializer.is_valid():
                reply = reply_serializer.save()
                replies.append(reply)

        return replies


class LikeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user_id = self.context['user_id']
        return models.Like.objects.create(user_id=user_id, **validated_data)

    class Meta:
        model = models.Like
        fields = ['id',  'user_id', 'content_type', 'object_id', 'is_liked']


class ReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    reply_date = serializers.SerializerMethodField()

    def get_reply_date(self, obj):
        return datetime.strftime(obj.reply_date, '%b %d, %Y %I:%M%p')

    def create(self, validated_data):
        user_id = self.context['user_id']
        return models.Reply.objects.create(user_id=user_id, **validated_data)

    class Meta:
        model = models.Reply
        fields = ['id', 'comment', 'user', 'message', 'reply_date']


class CustomReplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    reply_date = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.get_full_name()
        }

    def get_reply_date(self, obj):
        return datetime.strftime(obj.reply_date, '%b %d, %Y %I:%M%p')

    class Meta:
        model = models.Reply
        fields = ['id', 'user', 'message', 'reply_date']


class CommentSerializer(serializers.ModelSerializer):
    replies = CustomReplySerializer(
        source='reply_set',
        many=True,
        read_only=True,
    )
    user = serializers.SerializerMethodField()
    comment_date = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.get_full_name()
        }

    def get_comment_date(self, obj):
        return datetime.strftime(obj.comment_date, '%b %d, %Y %I:%M%p')

    def create(self, validated_data):
        user_id = self.context['user_id']
        return models.Comment.objects.create(user_id=user_id, **validated_data)

    class Meta:
        model = models.Comment
        fields = ['id',  'user', 'content_type',
                  'object_id', 'message', 'comment_date', 'replies']
