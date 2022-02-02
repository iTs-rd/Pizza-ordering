from django.contrib import admin

from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'size', 'quantity')
    list_filter = ['customer', 'status', 'size', 'quantity']
    search_fields = ['address', 'toppings']
    actions_on_bottom = True


admin.site.register(Order, OrderAdmin)
