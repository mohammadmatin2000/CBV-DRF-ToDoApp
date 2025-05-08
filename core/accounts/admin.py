from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Profile

# ======================================================================================================================
# CustomUserAdmin: A custom admin configuration for managing User model instances
class CustomUserAdmin(UserAdmin):
    """
    This class customizes the Django admin panel for user management.
    """

    model = User  # Specifies the model that this admin configuration applies to

    list_display = ("email", "is_staff", "is_active","is_verified")
    # Defines the fields visible in the admin list view.

    list_filter = ("email", "is_staff", "is_active","is_verified")
    # Adds filtering options in the admin panel to sort users by email, staff status, and active status.

    search_fields = ("email",)
    # Enables searching users by email in the admin panel.

    ordering = ("email",)
    # Sets the default ordering of users by email.

    fieldsets = (
        ('Authentication', {  # Section containing authentication-related fields
            'fields': ('email', 'password')  # Displays email and password fields in the admin panel
        }),
        ('Permissions', {  # Section for managing user permissions
            'fields': ('is_staff', 'is_superuser', 'is_active','is_verified')  # Controls access levels within the application
        }),
        ('Group Permissions', {  # Section for assigning groups and specific user permissions
            'fields': ('groups', 'user_permissions')  # Allows for role-based access control
        }),
        ('Important Date', {  # Section for tracking login activity
            'fields': ('last_login',)  # Displays the last login timestamp for users
        })
    )

    # Configuration for adding a new user from the admin panel
    add_fieldsets = (
        (None, {
            "classes": ("wide",),  # Applies styling for a clearer form layout
            "fields": (
                "email", "password1", "password2", "is_staff",  # Defines required fields for user creation
                "is_active", "is_superuser",
            )}
         ),
    )

# ======================================================================================================================
# Registers the User model with the admin site using the customized CustomUserAdmin configuration
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
# ======================================================================================================================