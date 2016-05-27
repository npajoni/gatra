from django.contrib import admin

# Register your models here.
from .models import Play
from .models import Event
from .models import Hash

@admin.register(Play)
class PlayConfig(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'title']
@admin.register(Event)
class EventConfig(admin.ModelAdmin):
    list_display = ['id', 'play', 'type', 'position']
    search_fields = ['play__user_name']
admin.site.register(Hash)
