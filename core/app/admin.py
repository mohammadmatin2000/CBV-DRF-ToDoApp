from django.contrib import admin
from .models import ToDoApp
# ======================================================================================================================
class ToDoAppAdmin(admin.ModelAdmin):
    list_display = ('author','content')
    list_filter = ('author','content')

# ======================================================================================================================
admin.site.register(ToDoApp,ToDoAppAdmin)
