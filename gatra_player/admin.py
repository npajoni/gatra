from django.contrib import admin

# Register your models here.
from .models import Play
from .models import Event
from .models import Hash

@admin.register(Play)
class PlayConfig(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'title']
    search_fields = ['user_name']

@admin.register(Event)
class EventConfig(admin.ModelAdmin):
    list_display = ['id', 'play', 'type', 'position']
    search_fields = ['play__user_name']

@admin.register(Hash)
class HashConfig(admin.ModelAdmin):
    list_display = ['valid_hash', 'user_name', 'title']

