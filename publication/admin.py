from datetime import datetime
from django.contrib import admin
from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Concat
from django.db.models.aggregates import Count
from django.utils.html import format_html
from . cache_handler import delete_cache_with_key_prefix
from . import models


@admin.register(models.Reader)
class ReaderAdmin(admin.ModelAdmin):
    fields = ['user', 'birthdate', 'city', 'country']
    list_display = ['avatar_diplay', 'user', 'birthdate', 'city', 'country']
    list_filter = ['city', 'country', 'birthdate']
    list_per_page = 10
    ordering = ['user']
    readonly_fields = ['user_avatar']
    search_fields = ['user__last_name',
                     'user__first_name', 'city', 'country']

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.insert(0, 'user_avatar')
        return super().get_fields(request, obj)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj:
            readonly_fields.insert(0, 'user')
        return readonly_fields

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def user_avatar(self, instance):
        if instance.user.avatar.name != '':
            return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')
        else:
            if instance.user.sex == 'N':
                instance.user.avatar = 'core/images/default_no_sex.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')
            elif instance.user.sex == 'M':
                instance.user.avatar = 'core/images/default_male.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')
            elif instance.user.sex == 'F':
                instance.user.avatar = 'core/images/default_female.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')

    @admin.display(ordering='id', description='User Avatar')
    def avatar_diplay(self, instance):
        if instance.user.avatar.name != '':
            return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')
        else:
            if instance.user.sex == 'N':
                instance.user.avatar = 'core/images/default_no_sex.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')
            elif instance.user.sex == 'M':
                instance.user.avatar = 'core/images/default_male.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')
            elif instance.user.sex == 'F':
                instance.user.avatar = 'core/images/default_female.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')

    class Media:
        css = {
            'all': ['publication/styles.css']
        }


class AuthorPositionInline(admin.StackedInline):
    autocomplete_fields = ['position']
    extra = 0
    min_num = 1
    model = models.AuthorPosition
    verbose_name = 'Position'


@ admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    actions = ['activate', 'deactivate']
    autocomplete_fields = ['user']
    fields = ['user', 'pen_name', 'is_active', 'note']
    exclude = ['date_updated']
    inlines = [AuthorPositionInline]
    list_display = ['avatar_diplay', 'user', 'pen_name',
                    'current_position', 'date_updated', 'is_active']
    list_filter = ['date_updated', 'is_active']
    list_per_page = 10
    ordering = ['-date_updated']
    readonly_fields = ['author_avatar', 'date_updated', 'note']
    search_fields = ['user__last_name',
                     'user__first_name', 'pen_name']

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.insert(0, 'author_avatar')
            fields.insert(3, 'date_updated')
        return fields

    def get_queryset(self, request):
        subquery = models.AuthorPosition.objects.select_related('position'). \
            filter(author_id=OuterRef('pk')). \
            order_by('-date_assigned'). \
            values('position__title')[:1]
        return super().get_queryset(request). \
            select_related('user') . \
            filter(user__is_active=True) . \
            annotate(current_position=Subquery(subquery))

    def save_model(self, request, obj, form, change):
        delete_cache_with_key_prefix('authors_list')
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    def author_avatar(self, instance):
        if instance.user.avatar.name != '':
            return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')
        else:
            if instance.user.sex == 'N':
                instance.user.avatar = 'core/images/default_no_sex.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')
            elif instance.user.sex == 'M':
                instance.user.avatar = 'core/images/default_male.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')
            elif instance.user.sex == 'F':
                instance.user.avatar = 'core/images/default_female.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile"/>')

    @admin.display(ordering='id', description="Author Avatar")
    def avatar_diplay(self, instance):
        if instance.user.avatar.name != '':
            return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')
        else:
            if instance.user.sex == 'N':
                instance.user.avatar = 'core/images/default_no_sex.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')
            elif instance.user.sex == 'M':
                instance.user.avatar = 'core/images/default_male.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')
            elif instance.user.sex == 'F':
                instance.user.avatar = 'core/images/default_female.jpg'
                return format_html(f'<img src="{instance.user.avatar.url}" class="profile_icon"/>')

    @ admin.display(ordering='current_position')
    def current_position(self, author):
        return author.current_position

    @admin.display(description='Note:')
    def note(self, article):
        """A friendly reminder to user """
        return format_html(f'''<i class="note">Author's positions section can be found by clicking the <b>blue "->" arrow</b> at the top of this form.</i>''')

    # SET MEMBER TO INACTIVE(vice-versa) INSTEAD OF DELETING
    @admin.action(description='Set selected authors to active')
    def activate(self, request, queryset):
        delete_cache_with_key_prefix('authors_list')
        queryset.update(is_active=True)

    @admin.action(description='Set selected authors to inactive')
    def deactivate(self, request, queryset):
        delete_cache_with_key_prefix('authors_list')
        queryset.update(is_active=False)
    # ========================================

    class Media:
        css = {
            'all': ['publication/styles.css']
        }


@admin.register(models.Contributor)
class ContributorAdmin(admin.ModelAdmin):
    fields = ['name_or_pen_name']
    list_display = ['id', 'name_or_pen_name', 'date_added', 'articles_count']
    list_filter = ['date_added']
    list_per_page = 10
    ordering = ['-date_added']
    readonly_fields = ['date_added', 'articles_count']
    search_fields = ['name_or_pen_name']

    def has_delete_permission(self, request, obj=None):
        return False

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.append('date_added')
            fields.append('articles_count')
        return fields

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(articles_count=Count('article'))

    @admin.display(ordering='articles_count', description='Number of Articles')
    def articles_count(self, contributor: models.Contributor):
        return contributor.articles_count


@ admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'position', 'authors_count']
    search_fields = ['title']

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(authors_count=Count('authorposition__author'))

    @admin.display(ordering='title')
    def position(self, position):
        return position.title

    @admin.display(ordering='authors_count', description='Number of Authors')
    def authors_count(self, position: models.Position):
        return position.authors_count


@admin.register(models.AuthorPosition)
class AuthorPositionAdmin(admin.ModelAdmin):
    fields = ['author', 'position']
    list_display = ['id', 'author', 'position', 'date_assigned']
    list_filter = ['date_assigned', 'author']
    list_select_related = ['author__user', 'position']
    ordering = ['-date_assigned']
    readonly_fields = ['date_assigned']
    search_fields = ['author__user__first_name', 'author__user__middle_initial',
                     'author__user__last_name', 'position__title']

    def has_delete_permission(self, request, obj=None):
        return False

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.append('date_assigned')
        return fields


@admin.register(models.Update)
class UpdateAdmin(admin.ModelAdmin):
    actions = ['post', 'remove_post']
    fields = ['title', 'description', 'image', 'image_caption', 'is_posted']
    list_display = ['thumbnail_display', 'title', 'update_description',
                    'posted_by', 'date_created', 'date_posted', 'is_posted']
    list_filter = ['is_posted', 'member', 'date_created']
    list_per_page = 10
    list_select_related = ['member__user']
    ordering = ['-is_posted', '-date_posted']
    readonly_fields = ['created_by',
                       'date_created', 'thumbnail', 'date_posted']
    search_fields = ['image', 'member__user__first_name',
                     'member__user__middle_initial', 'member__user__last_name']

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.insert(2, 'created_by')
            fields.insert(3, 'date_created')
            fields.insert(4, 'thumbnail')
            if obj.is_posted:
                fields.append('date_posted')
        return fields

    def save_model(self, request, obj, form, change):
        if obj.is_posted:
            obj.date_posted = datetime.now().date()
        if not obj.is_posted:
            obj.date_posted = None
        obj.member = request.user.author
        delete_cache_with_key_prefix('updates_list')
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(ordering='description', description='description')
    def update_description(self, update: models.Update):
        description = update.description
        if len(description) > 50:
            description = description[:50]
            return description.rstrip() + '...'
        return description

    @admin.display(ordering='id', description='update image')
    def thumbnail_display(self, update: models.Update):
        if update.image.name == '':
            update.image = 'publication/update/images/default_update.png'
        return format_html(f'<img src="{update.image.url}" class="update"/>')

    @admin.display(description='update image')
    def thumbnail(self, update: models.Update):
        return format_html(f'<img src="{update.image.url}" class="thumbnail"/>')

    @admin.display(ordering='member', description='created by')
    def posted_by(self, update: models.Update):
        return update.member

    def created_by(self, update: models.Update):
        return update.member

    @ admin.action(description='Post selected updates')
    def post(self, request, queryset):
        updated_count = queryset.update(
            is_posted=True,
            date_posted=datetime.now().date(),
        )
        self.message_user(
            request,
            f'{updated_count} updates were successfully posted.',
            "success"
        )
        delete_cache_with_key_prefix('updates_list')

    @ admin.action(description='Remove selected updates from posts')
    def remove_post(self, request, queryset):
        updated_count = queryset.update(
            is_posted=False,
            date_posted=None,
        )
        self.message_user(
            request,
            f'{updated_count} updates were removed from posts.',
            "error"
        )
        delete_cache_with_key_prefix('updates_list')

    class Media:
        css = {
            'all': ['publication/styles.css']
        }


class IsEnabledFilter(admin.SimpleListFilter):
    """- a custom filter for 'is_enabled' field"""
    title = 'display'
    parameter_name = 'display'

    def lookups(self, request, model_admin):
        return [
            ('Yes', 'Enabled'),
            ('No', 'Disabled')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(is_enabled=True)
        elif self.value() == 'No':
            return queryset.filter(is_enabled=False)


class IsPostedFilter(admin.SimpleListFilter):
    """- a custom filter for 'is_posted' field"""
    title = 'post status'
    parameter_name = 'is_posted'

    def lookups(self, request, model_admin):
        return [
            ('Yes', 'Posted'),
            ('No', 'Not Posted')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(is_posted=True)
        elif self.value() == 'No':
            return queryset.filter(is_posted=False)


class IssueFileInline(admin.StackedInline):
    fields = ['issue', 'file', 'image_for_thumbnail']
    max_num = 1
    min_num = 1
    model = models.IssueFile
    readonly_fields = ['thumbnail']
    verbose_name_plural = 'Issue'

    def thumbnail(self, instance):
        if instance.image_for_thumbnail.name != '':
            return format_html(f'<img src="{instance.image_for_thumbnail.url}" class="thumbnail"/>')
        return ''

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.append('thumbnail')
        return fields

    def has_delete_permission(self, request, obj=None):
        return False


@ admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    actions = ['post', 'remove_post']
    fields = ['volume_number', 'issue_number', 'date_published',
              'category', 'description', 'end_date', 'note']
    inlines = [IssueFileInline]
    list_display = ['id', 'volume_number', 'issue_number', 'uploaded_by',
                    'category', 'date_updated', 'date_published', 'is_posted', 'is_enabled']
    list_filter = ['category', IsPostedFilter,
                   IsEnabledFilter, 'date_published', 'date_created', 'date_updated']
    list_per_page = 10
    list_select_related = ['uploaded_by__user', 'issuefile']
    ordering = ['-is_posted', '-date_published']
    readonly_fields = ['uploaded_by', 'date_created', 'date_updated', 'note']
    search_fields = ['volume_number__contains', 'issue_number__contains', 'description',
                     'uploaded_by__user__last_name__istartswith', 'uploaded_by__user__first_name__istartswith', 'uploaded_by__pen_name__istartswith']

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # for disabling due issue
        for issue in queryset:
            # for checking duration
            if issue.end_date <= datetime.now().date():
                issue.is_enabled = False
                issue.save()
            else:
                issue.is_enabled = True
                issue.save()
        return queryset

    def get_actions(self, request):
        actions = super().get_actions(request)
        # for removing approval and display action if no permission
        if not request.user.has_perms(['publication.can_post_issue',
                                       'publication.can_remove_issue_post']):
            del actions['post']
            del actions['remove_post']
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.insert(3, 'date_created')
            fields.insert(4, 'date_updated')
            fields.insert(8, 'uploaded_by')
        return fields

    def delete_queryset(self, request, queryset):
        delete_cache_with_key_prefix('issues_list')
        return super().delete_queryset(request, queryset)

    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user.author
        delete_cache_with_key_prefix('issues_list')
        return super().save_model(request, obj, form, change)

    @admin.display(ordering='uploaded_by')
    def uploaded_by(self, issue):
        return issue.uploaded_by

    @admin.display(description='Note:')
    def note(self, article):
        """A friendly reminder to user """
        return format_html(f'''<i class="note">Issue's file section can be found by clicking the <b>blue "->" arrow</b> at the top of this form.</i>''')

    @ admin.action(description='Post selected issues')
    def post(self, request, queryset):
        updated_count = queryset.update(is_posted=True)
        self.message_user(
            request,
            f'{updated_count} issues were successfully posted.',
            "success"
        )
        delete_cache_with_key_prefix('issues_list')

    @ admin.action(description='Remove selected issues from posts')
    def remove_post(self, request, queryset):
        updated_count = queryset.update(is_posted=False)
        self.message_user(
            request,
            f'{updated_count} issues were removed from posts.',
            "error"
        )
        delete_cache_with_key_prefix('issues_list')

    class Media:
        css = {
            'all': ['publication/styles.css']
        }


class IsPostedFilter(admin.SimpleListFilter):
    """- a custom filter for 'is_posted' field"""
    title = 'post status'
    parameter_name = 'is_posted'

    def lookups(self, request, model_admin):
        return [
            ('Yes', 'Posted'),
            ('No', 'Not Posted')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(is_posted=True)
        elif self.value() == 'No':
            return queryset.filter(is_posted=False)


class IsEnabledFilter(admin.SimpleListFilter):
    """- a custom filter for 'is_enabled' field"""
    title = 'display'
    parameter_name = 'display'

    def lookups(self, request, model_admin):
        return [
            ('Yes', 'Enabled'),
            ('No', 'Disabled')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(is_enabled=True)
        elif self.value() == 'No':
            return queryset.filter(is_enabled=False)


class BannerInline(admin.TabularInline):
    extra = 0
    fields = ['image']
    model = models.Banner
    readonly_fields = ['thumbnail', 'member']
    verbose_name = 'Banner'
    verbose_name_plural = 'Banner'

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="banner"/>')
        return 'No Image Yet'

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.insert(0, 'thumbnail')
            fields.append('member')
        return fields


class ArticleImageInline(admin.TabularInline):
    extra = 0
    fields = ['article', 'image', 'image_caption']
    max_num = 3
    model = models.ArticleImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return 'No Image Yet'

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.insert(0, 'thumbnail')
        return fields


class ContributorInline(admin.TabularInline):
    model = models.Article.contributors.through
    extra = 0
    verbose_name = 'Contributor'
    verbose_name_plural = 'Contributors'


class AuthorsInline(admin.TabularInline):
    model = models.Article.authors.through
    extra = 0
    verbose_name = 'Author'
    verbose_name_plural = 'Authors'


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    actions = ['post', 'remove_post']
    fields = ['title_or_headline', 'slug', 'date_published',
              'category', 'body', 'end_date', 'is_highlight', 'note']
    inlines = [ArticleImageInline, ContributorInline,
               AuthorsInline, BannerInline,]
    list_display = ['id', 'title_or_headline', 'author', 'contributor', 'category',
                    'date_updated', 'date_published', 'is_posted', 'is_enabled', 'is_highlight']
    list_filter = ['category', IsPostedFilter, IsEnabledFilter,
                   'date_published', 'date_created', 'date_updated']
    list_per_page = 10
    ordering = ['is_posted', '-date_published']
    prepopulated_fields = {
        'slug': ['title_or_headline']
    }
    readonly_fields = ['uploaded_by', 'date_created', 'date_updated', 'note']
    search_fields = ['title_or_headline', 'authors__user__last_name',
                     'authors__user__first_name', 'body', 'contributors__name_or_pen_name']

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, models.Banner):
                if instance.pk is None:  # check if instance is newly added
                    instance.member = request.user.author
                instance.save()
            else:
                instance.save()
        for instance in formset.deleted_objects:
            instance.delete()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user.author
        delete_cache_with_key_prefix('articles_list')
        delete_cache_with_key_prefix('banners_list')
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        # for removing approval and display action if no permission
        if not request.user.has_perms(['publication.can_post_article',
                                       'publication.can_remove_article_post']):
            del actions['post']
            del actions['remove_post']
        return actions

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.insert(3, 'date_created')
            fields.insert(4, 'date_updated')
            fields.insert(8, 'uploaded_by')
        return fields

    def get_queryset(self, request):
        first_author = models.Article.objects. \
            filter(authors=OuterRef('pk')). \
            values('authors__user__first_name', 'authors__user__last_name'). \
            annotate(full_name=Concat('authors__user__first_name',
                                      Value(' '),
                                      'authors__user__last_name',
                                      ))[:1]
        first_contributor = models.Article.objects. \
            filter(contributors=OuterRef('pk')). \
            values('contributors__name_or_pen_name')[:1]
        first_author = first_author.values('full_name')
        queryset = super().get_queryset(request). \
            select_related('uploaded_by__user'). \
            prefetch_related('authors__user', 'article_images', 'contributors'). \
            annotate(contributor_full_name=Subquery(first_contributor)). \
            annotate(author_full_name=Subquery(first_author))
        # for disabling due articles
        for article in queryset:
            # for checking duration
            if article.end_date <= datetime.now().date():
                article.is_enabled = False
                article.save()
            else:
                article.is_enabled = True
                article.save()
        return queryset

    @admin.display(ordering='author_full_name', description='Author/s')
    def author(self, article):
        if len(article.authors.all()) == 0:
            return 'None'
        return format_html(",<br>".join([str(author) for author in article.authors.all()]))

    @admin.display(ordering='contributor_full_name', description='Contributor/s')
    def contributor(self, article):
        if len(article.contributors.all()) == 0:
            return 'None'
        return format_html(",<br>".join([str(contributor) for contributor in article.contributors.all()]))

    @admin.action(description='Post selected articles')
    def post(self, request, queryset):
        updated_count = queryset.update(is_posted=True)
        self.message_user(
            request,
            f'{updated_count} articles were successfully posted.',
            "success"
        )
        delete_cache_with_key_prefix('articles_list')

    @ admin.action(description='Remove selected articles from posts')
    def remove_post(self, request, queryset):
        updated_count = queryset.update(is_posted=False)
        self.message_user(
            request,
            f'{updated_count} articles were removed from posts.',
            "error"
        )
        delete_cache_with_key_prefix('articles_list')

    def uploaded_by(self, article):
        return article.uploaded_by

    @admin.display(description='Note:')
    def note(self, article):
        """A friendly reminder to user """
        return format_html(f'<i class="note">Athors, Contributors, and Article Images section can be found by clicking the <b>blue arrows</b> at the top of this form.</i>')

    class Media:
        css = {
            'all': ['publication/styles.css']
        }


@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    # actions = ['post', 'remove_post']
    fields = ['article', 'image']
    list_display = ['thumbnail_display',
                    'article', 'posted_by', 'date_created']
    list_filter = ['member', 'date_created']
    list_select_related = ['member__user', 'article']
    ordering = ['-date_created']
    readonly_fields = ['created_by', 'date_created', 'thumbnail']
    search_fields = ['image', 'member__user__first_name',
                     'member__user__middle_initial', 'member__user__last_name']

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.insert(1, 'created_by')
            fields.insert(2, 'date_created')
            fields.insert(3, 'thumbnail')
        return fields

    def save_model(self, request, obj, form, change):
        obj.member = request.user.author
        delete_cache_with_key_prefix('banners_list')
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(ordering='id', description='banner image')
    def thumbnail_display(self, banner: models.Banner):
        return format_html(f'<img src="{banner.image.url}" class="update"/>')

    @admin.display(description='banner image')
    def thumbnail(self, banner: models.Banner):
        return format_html(f'<img src="{banner.image.url}" class="banner"/>')

    @ admin.display(ordering='member', description='created by')
    def posted_by(self, banner: models.Banner):
        return banner.member

    def created_by(self, banner: models.Banner):
        return banner.member

    # @ admin.action(description='Post selected banners')
    # def post(self, request, queryset):
    #     updated_count = queryset.update(is_posted=True)
    #     self.message_user(
    #         request,
    #         f'{updated_count} banners were successfully posted.',
    #         "success"
    #     )
    #     delete_cache_with_key_prefix('banners_list')

    # @ admin.action(description='Remove selected banners from posts')
    # def remove_post(self, request, queryset):
    #     updated_count = queryset.update(is_posted=False)
    #     self.message_user(
    #         request,
    #         f'{updated_count} banners were removed from posts.',
    #         "error"
    #     )
    #     delete_cache_with_key_prefix('banners_list')

    class Media:
        css = {
            'all': ['publication/styles.css']
        }
