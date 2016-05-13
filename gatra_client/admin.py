
from django.contrib import admin

# Register your models here.
from .models import UserLog



@admin.register(UserLog)
class LoginConfig(admin.ModelAdmin):
    list_display = ['date','source_ip','customer_name', 'customer_id', 'idp','access','user_agent']

