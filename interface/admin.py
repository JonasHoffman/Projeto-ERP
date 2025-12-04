from django.contrib import admin
from interface.models import MenuItem
# Register your models here.
@admin.register(MenuItem)
class MenuAdmin(admin.ModelAdmin):
    ...