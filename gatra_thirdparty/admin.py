from django.contrib import admin

# Register your models here.
from .models import Play

@admin.register(Play)
class PlayConfig(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'title']
    search_fields = ['user_name']
