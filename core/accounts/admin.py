from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from  .models import User
# ======================================================================================================================
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email","is_staff","is_active",)
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        ('Authentication', {  # Section for authentication-related fields
            'fields': ('email', 'password')
        }),
        ('Permissions', {  # Section for managing access control
            'fields': ('is_staff', 'is_superuser', 'is_active')
        }),
        ('Group Permissions', {  # Section for assigning group and user permissions
            'fields': ('groups', 'user_permissions')
        }),
        ('Important Date', {  # Section for tracking login activity
            'fields': ('last_login',)
        })
    )

    # Configuration for adding a new user from the admin panel
    add_fieldsets = (
        (None, {
            "classes": ("wide",),  # Styling applied to the form
            "fields": (
                "email", "password1", "password2", "is_staff",  # Required fields for creating a new user
                "is_active", "is_superuser",
            )}
         ),
    )
# ======================================================================================================================
admin.site.register(User, CustomUserAdmin)