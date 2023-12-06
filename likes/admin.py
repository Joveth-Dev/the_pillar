import urllib.parse
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from . import models

# filter for article & issue


class IsArticleorIssueFilter(admin.SimpleListFilter):
    """- a custom filter for 'is_enabled' field"""
    title = 'article | issue'
    parameter_name = 'content_type'

    def lookups(self, request, model_admin):
        return [
            ('article', 'Article'),
            ('issue', 'Issue')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'article':
            return queryset.filter(content_type=8)
        elif self.value() == 'issue':
            return queryset.filter(content_type=9)


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    fields = ['content_type', 'object_id', 'is_liked']
    list_display = ['id', 'item_name', 'reacted_by', 'is_liked']
    list_filter = ['is_liked']
    list_per_page = 10
    list_select_related = ['content_type', 'user']
    search_fields = ['object_id', 'user__first_name__icontains',
                     'user__middle_initial__icontains', 'user__last_name__icontains']

    def save_model(self, request, obj, form, change):
        if not change and models.Like.objects.filter(user=request.user, object_id=obj.object_id).exists():
            self.message_user(
                request,
                "You already reacted on this article.",
                "error"
            )
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(ordering='content_object', description='Article Title')
    def item_name(self, like):
        return like.content_object

    @admin.display(ordering='user__username')
    def reacted_by(self, like):
        return like.user


class ReplyInline(admin.TabularInline):
    extra = 0
    fields = ['user', 'reply_date', 'message']
    model = models.Reply
    readonly_fields = ['user', 'reply_date']
    show_change_link = True
    verbose_name_plural = 'Replies'


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ['content_type', 'object_id', 'message', 'note']
    inlines = [ReplyInline]
    list_display = ['id', 'item_name', 'comment_message',
                    'commented_by', 'comment_date', 'count_reply']
    list_filter = ['comment_date']
    list_per_page = 10
    ordering = ['-comment_date']
    readonly_fields = ['user', 'note']
    search_fields = ['user__first_name__icontains', 'user__middle_initial__icontains',
                     'user__last_name__icontains', 'message__icontains']

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_queryset(self, request):
        return super().get_queryset(request). \
            select_related('user', 'content_type'). \
            prefetch_related('reply_set'). \
            annotate(count_reply=Count('reply'))

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.insert(0, 'user')
        return fields

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj:
            readonly_fields.append('content_type')
            readonly_fields.append('object_id')
            if obj.user != request.user:
                readonly_fields.append('message')
        return readonly_fields

    def get_inline_formsets(self, request, formsets, inline_instances, obj):
        for formset, inline in zip(formsets, inline_instances):
            for form in formset:
                if isinstance(inline, ReplyInline) and request.user != form.instance.user:
                    form.fields['message'].widget.attrs['readonly'] = True
                    form.fields['message'].widget.attrs['title'] = 'Read-only'
        return super().get_inline_formsets(request, formsets, inline_instances, obj)

    def save_model(self, request, obj: models.Comment, form, change):
        if not change:
            obj.user = request.user
        return super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            if formset.model == models.Reply:
                instances = formset.save(commit=False)
                for instance in instances:
                    if instance.pk is None:
                        instance.save(request=request)
                formset.save()
            else:
                formset.save()

    @admin.display(ordering='user')
    def commented_by(self, comment):
        return comment.user.get_full_name()

    # @admin.display(ordering='object_id', description='Post ID')
    # def item_id(self, comment):
    #     return comment.object_id

    # @admin.display(ordering='content_type', description='Post Type')
    # def item_type(self, comment):
    #     return comment.content_type.model

    @admin.display(ordering='content_object', description='article title')
    def item_name(self, comment):
        return comment.content_object

    @admin.display(ordering='count_reply', description='Number of Replies')
    def count_reply(self, comment: models.Comment):
        return comment.count_reply

    @admin.display(ordering='comment_message', description='comment')
    def comment_message(self, comment: models.Comment):
        comment = urllib.parse.unquote(comment.message)
        if len(comment) > 50:
            comment = comment[:50]
            return comment.rstrip() + '...'
        return comment

    @admin.display(description='Note:')
    def note(self, article):
        """A friendly reminder to user """
        return format_html(f'''<i class="note">Replies section can be found by clicking the <b>blue "->" arrow</b> at the top of this form.</i>''')


@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    fields = ['comment', 'message']
    list_display = ['id', 'comment_message',
                    'reply_message', 'reply_by', 'reply_date']
    list_filter = ['user', 'reply_date']
    list_per_page = 10
    list_select_related = ['comment', 'user']
    ordering = ['-reply_date']
    readonly_fields = ['user', 'reply_date']
    search_fields = ['user__first_name__icontains', 'user__middle_initial__icontains',
                     'user__last_name__icontains', 'message__icontains']

    def save_model(self, request, obj: models.Reply, form, change):
        if not change:
            obj.user = request.user
        return super().save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        fields = list(self.fields)
        if obj:
            fields.insert(1, 'user')
            fields.insert(2, 'reply_date')
        return fields

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj:
            readonly_fields.insert(0, 'comment')
        return readonly_fields

    def has_change_permission(self, request, obj=None):
        if obj and obj.user != request.user:
            return False
        return super().has_change_permission(request, obj)

    # def has_add_permission(self, request):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    @admin.display(ordering='comment_message', description='comment')
    def comment_message(self, reply: models.Reply):
        comment = reply.comment.message
        if len(comment) > 50:
            comment = comment[:50]
            return comment.rstrip() + '...'
        return comment

    @admin.display(ordering='message', description='reply')
    def reply_message(self, reply: models.Reply):
        message = reply.message
        if len(message) > 50:
            message = message[:50]
            return message.rstrip() + '...'
        return message

    @admin.display(ordering='user')
    def reply_by(self, reply: models.Reply):
        return reply.user
