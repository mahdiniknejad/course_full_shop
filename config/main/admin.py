from django.contrib import admin
from .models import Cart, SubCart
# Register your models here.


class SubCartAdmin(admin.TabularInline):
    model = SubCart


class CartAdmin(admin.ModelAdmin):
    list_display = ['__str__',]

    inlines = [
        SubCartAdmin,
    ]

admin.site.register(Cart, CartAdmin)
