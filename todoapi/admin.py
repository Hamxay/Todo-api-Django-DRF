from django.contrib import admin

from .models import Todo

# Register your models here.


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'title', 'description', 'datetime']
# admin.site.register(Todo)
