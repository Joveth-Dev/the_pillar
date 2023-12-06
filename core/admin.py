from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from . import models

# NEED TO CUSTOMIZE PRESENTATION IN ADMIN


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_flag', 'user',
                    'object_repr', 'action_time', 'change_message']
    list_filter = ['action_time', 'action_flag']
    list_per_page = 20
    list_select_related = ['user', 'content_type']
    search_fields = ['user__first_name__icontains', 'user__middle_initial__icontains',
                     'user__last_name__icontains', 'change_message__icontains']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# unregister default group model in the admin panel
admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    list_display = ['id', 'name']
    list_per_page = 10
    search_fields = ['name__icontains']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('permissions')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'content_type', 'codename']
    list_per_page = 10
    list_select_related = ['content_type']
    search_fields = ['name__icontains']

    # def has_add_permission(self, request):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    # SET USER TO INACTIVE INSTEAD OF DELETING
    def delete_queryset(self, request, queryset):
        queryset.update(is_active=False)
    # ========================================

    actions = ['delete_user']
    list_display = ['avatar_display', 'username', 'first_name',
                    'middle_initial', 'last_name', 'email', 'sex', 'is_staff', 'is_active']
    list_filter = ("is_staff", "is_active", "groups", 'sex')
    list_per_page = 10
    fieldsets = (
        (None, {"fields": ("username", "password", 'note')}),
        (_("Personal info"), {
         "fields": ('user_avatar', 'avatar', "first_name", 'middle_initial', "last_name", "email", 'sex')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    # "is_superuser",
                    "groups",
                    # "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'last_name', 'first_name', 'middle_initial'),
            },
        ),
    )
    readonly_fields = ['user_avatar', 'note']
    search_fields = ['username__icontains', 'first_name__icontains',
                     'middle_initial__icontains', 'last_name__icontains', 'email__icontains']

    def has_delete_permission(self, request, obj=None):
        return False

    def user_avatar(self, instance):
        if instance.avatar.name != '':
            return format_html(f'<img src="{instance.avatar.url}" class="profile"/>')
        else:
            if instance.sex == 'N':
                instance.avatar = 'core/images/default_no_sex.jpg'
                return format_html(f'<img src="{instance.avatar.url}" class="profile"/>')
            elif instance.sex == 'M':
                instance.avatar = 'core/images/default_male.jpg'
                return format_html(f'<img src="{instance.avatar.url}" class="profile"/>')
            elif instance.sex == 'F':
                instance.avatar = 'core/images/default_female.jpg'
                return format_html(f'<img src="{instance.avatar.url}" class="profile"/>')

    @admin.display(ordering='id', description='User Avatar')
    def avatar_display(self, instance):
        if instance.avatar.name != '':
            return format_html(f'<img src="{instance.avatar.url}" class="profile_icon"/>')
        else:
            if instance.sex == 'N':
                instance.avatar = 'core/images/default_no_sex.jpg'
                return format_html(f'<img src="{instance.avatar.url}" class="profile_icon"/>')
            elif instance.sex == 'M':
                instance.avatar = 'core/images/default_male.jpg'
                return format_html(f'<img src="{instance.avatar.url}" class="profile_icon"/>')
            elif instance.sex == 'F':
                instance.avatar = 'core/images/default_female.jpg'
                return format_html(f'<img src="{instance.avatar.url}" class="profile_icon"/>')

    @admin.display(description='Note:')
    def note(self, article):
        """A friendly reminder to user """
        return format_html(f'''<i class="note">User's Personal Info, Permissions, and Important Dates section can be found by clicking the <b>blue arrows</b> at the top of this form.</i>''')

    class Media:
        css = {
            'all': ['core/styles.css']
        }
