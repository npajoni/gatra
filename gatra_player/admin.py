from django.contrib import admin

# Register your models here.
from .models import Play
from .models import Event
from .models import Hash

@admin.register(Play)
class PlayConfig(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'title']
admin.site.register(Event)
admin.site.register(Hash)
