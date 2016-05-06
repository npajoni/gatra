from django.contrib import admin

# Register your models here.
from .models import Play
from .models import Event
from .models import Hash

admin.site.register(Play)
admin.site.register(Event)
admin.site.register(Hash)
