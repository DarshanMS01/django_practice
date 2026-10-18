from re import search

from django.contrib import admin
from .models import department, employee
# Register your models here.
class employeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'department', 'salary', 'designation', 'joining_date', 'is_active', 'manager' )
    list_filter = ['manager']
    search_fields = ['first_name', 'last_name', 'email']
    list_editable = ['is_active']

    list_display_links = ('first_name', 'last_name', 'email')
    ordering = ["id"]

admin.site.register(department)
admin.site.register(employee, employeeAdmin)
