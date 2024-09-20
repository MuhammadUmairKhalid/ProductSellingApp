from django.contrib import admin
# Register your models here.
# from django.contrib.auth.models import User
from Auth.models import User
from django.contrib import admin

class ReadOnlyUserAdmin(admin.ModelAdmin):
    readonly_fields = ['username', 'email', 'password', 'user_type']  # Mark fields as read-only
    list_display = ['username', 'email','password', 'user_type']  # Fields to display in the list

    def has_add_permission(self, request):
        return False  # Prevent addition of new users

    def has_change_permission(self, request, obj=None):
        return False  # Prevent changes to existing users

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion of users

    def has_view_permission(self, request, obj=None):
        return True  # Allow viewing users

admin.site.register(User, ReadOnlyUserAdmin)

