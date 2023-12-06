from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .pagination import DefaultPagination, CommentPagination
from . import models, serializers, permissions


class LikeViewSet(ModelViewSet):
    queryset = models.Like.objects. \
        select_related('content_type', 'user')
    serializer_class = serializers.LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, permissions.IsCurrentUser]
    # pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_liked', 'user_id', 'object_id', 'content_type']

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            data = {'error': 'You already reacted on this article.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects. \
        select_related('content_type', 'user'). \
        prefetch_related('reply_set'). \
        order_by('-comment_date')
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, permissions.IsCurrentUser]
    pagination_class = CommentPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['content_type', 'user_id', 'object_id']

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class ReplyViewSet(ModelViewSet):
    queryset = models.Reply.objects. \
        select_related('user', 'comment'). \
        order_by('-reply_date')
    serializer_class = serializers.ReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, permissions.IsCurrentUser]
    # pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['comment', 'user_id']
    search_fields = ['message']

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
