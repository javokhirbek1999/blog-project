from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _


from api.models.user import User
from api.models.blog import Post



@admin.register(User)
class UserAdminConfig(UserAdmin):

    """User config for Admin Dashboard."""

    ordering = ['id']
    list_filter = ['id']
    list_display = ['email', 'first_name', 'last_name', 'date_joined', 'date_updated']
    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important Dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        })
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published')
    list_filter = ('published', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

    def author(self, obj):
        return obj.author.username
    author.short_description = 'Author'

    def get_queryset(self, request):
        """Limit posts displayed to those authored by the current user."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        """Allow change permission only for the user's own posts."""
        if obj is None:
            return True
        return obj.author == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Allow delete permission only for the user's own posts."""
        if obj is None:
            return True
        return obj.author == request.user or request.user.is_superuser

    def has_add_permission(self, request):
        """Allow add permission for all users."""
        return True
