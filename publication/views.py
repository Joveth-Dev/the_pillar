from django.db.models import OuterRef, Subquery
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from .pagination import DefaultPagination
from . import models, serializers, permissions


class AuthorViewSet(ReadOnlyModelViewSet):
    # get the current position of the members first
    subquery = models.AuthorPosition.objects.select_related('position') \
        .filter(author_id=OuterRef('pk')) \
        .order_by('-date_assigned') \
        .values('position__title')[:1]

    # annotate the queryset with their current position
    queryset = models.Author.objects.prefetch_related('authorposition_set') \
        .annotate(current_position=Subquery(subquery)) \
        .filter(user__is_active=True) \
        .filter(is_active=True) \
        .defer('date_updated')
    serializer_class = serializers.AuthorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__first_name', 'user__middle_initial',
                     'user__last_name', 'pen_name']

    @method_decorator(cache_page(10*60, key_prefix='authors_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# class ReaderViewSet(UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
#     queryset = models.Reader.objects.all()
#     serializer_class = serializers.ReaderSerializer
#     permission_classes = [permissions.IsCurrentUser]

#     @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
#     def me(self, request):
#         reader = models.Reader.objects.get(user_id=request.user.id)
#         if request.method == 'GET':
#             serializer = serializers.ReaderSerializer(reader)
#             return Response(serializer.data)
#         elif request.method == 'PUT':
#             serializer = serializers.ReaderSerializer(
#                 reader, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)


class IssueViewSet(ReadOnlyModelViewSet):
    queryset = models.Issue.objects \
        .select_related('issuefile') \
        .defer('date_created', 'is_posted', 'is_enabled') \
        .filter(is_posted=True) \
        .order_by('-date_published')
    # .filter(is_enabled=True) \
    serializer_class = serializers.IssueSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['date_published',
                       'date_updated', 'volume_number', 'issue_number']
    # pagination_class = DefaultPagination
    search_fields = ['volume_number', 'issue_number', 'description']

    @method_decorator(cache_page(10*60, key_prefix='issues_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ArticleViewSet(ReadOnlyModelViewSet):
    queryset = models.Article.objects \
        .select_related('uploaded_by__user') \
        .defer('authors__date_updated') \
        .defer('authors__user__password',
               'authors__user__last_login',
               'authors__user__is_superuser',
               'authors__user__username',
               'authors__user__is_staff',
               'authors__user__is_active',
               'authors__user__date_joined',
               'authors__user__email') \
        .prefetch_related('article_images', 'contributors', 'authors') \
        .defer('slug', 'date_created', 'is_posted', 'is_enabled') \
        .filter(is_posted=True) \
        .order_by('-is_highlight', '-date_published')
    # .filter(is_enabled=True)
    serializer_class = serializers.ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,
                       OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['date_published', 'date_published']
    # pagination_class = DefaultPagination
    search_fields = ['title_or_headline', 'body', 'authors__pen_name',
                     'authors__user__first_name', 'authors__user__last_name', 'contributors__name_or_pen_name']

    @method_decorator(cache_page(10*60, key_prefix='articles_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UpdateViewSet(ReadOnlyModelViewSet):
    queryset = models.Update.objects. \
        select_related('member'). \
        filter(is_posted=True). \
        order_by('-date_posted')
    filter_backends = [OrderingFilter]
    ordering_fields = ['-date_posted']
    serializer_class = serializers.UpdateSerializer

    @method_decorator(cache_page(10*60, key_prefix='updates_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BannerViewSet(ReadOnlyModelViewSet):
    queryset = models.Banner.objects. \
        select_related('member', 'article'). \
        filter(article__is_posted=True). \
        order_by('-date_created')
    filter_backends = [OrderingFilter]
    ordering_fields = ['-date_created']
    serializer_class = serializers.BannerSerializer

    @method_decorator(cache_page(10*60, key_prefix='banners_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
