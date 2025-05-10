from django.contrib import admin
from .models import ToDoApp


# ======================================================================================================================
# ToDoAppAdmin: Customizes the Django admin interface for managing ToDoApp model instances
class ToDoAppAdmin(admin.ModelAdmin):
    """
    This class defines how the ToDoApp model is displayed in the Django admin panel.
    """

    list_display = ("author", "content")
    # Specifies the fields that will be displayed in the admin list view.

    list_filter = ("author", "content")
    # Adds filter options in the admin panel, allowing tasks to be filtered by author and content.


# ======================================================================================================================
# Registers the ToDoApp model with the Django admin site using the custom ToDoAppAdmin configuration
admin.site.register(ToDoApp, ToDoAppAdmin)

# ======================================================================================================================
