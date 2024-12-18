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
    readonly_fields = ('date_joined', 'date_updated')

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name')}),
        (_('Important Dates'), {'fields': ('date_joined', 'date_updated')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    def get_queryset(self, request):
        """Limit users displayed to their own account, unless the user is a superuser."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)  # Limit to the logged-in user's account

    def has_change_permission(self, request, obj=None):
        """Allow change permission only for the user's own account."""
        if obj is None:  # When viewing the list of objects
            return True
        return obj.id == request.user.id or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Allow delete permission only for the user's own account."""
        if obj is None:  # When viewing the list of objects
            return True
        return obj.id == request.user.id or request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        """Allow view permission only for the user's own account."""
        if obj is None:  # When viewing the list of objects
            return True
        return obj.id == request.user.id or request.user.is_superuser

    def has_add_permission(self, request):
        """Disallow users from adding accounts in the admin."""
        return request.user.is_superuser  # Only superusers can add accounts



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published')
    list_filter = ('published', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        
        """Assign the current logged-in user as the athor of the currently being created post."""
        
        if not obj.pk: # If the object is being created
            obj.author = request.user
        
        super().save_model(request, obj, form, change)

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
