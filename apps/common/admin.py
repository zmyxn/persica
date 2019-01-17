from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Tree
from guardian.models import UserObjectPermission
# Register your models here.

class TreeAdmin(admin.ModelAdmin):
    # inlines = [BookInline,]
    # fieldsets = (
    #     (None, {'fields': ('username','ldap_name', 'email', 'work_phone')}),
    #     ('Personal info', {'fields': ('skill_level', 'air_levels', 'residence_levels')}),
    #     ('Group info', {'fields': ('department', 'position', 'rfid' ,'rfid_name')}),
    #     ('visa info', {'fields': ('visa_status', 'visa_issue_date', 'visa_expir_date')}),
    #     ('Permissions', {'fields': ('is_active', 'is_staff','is_superuser', 'user_permissions','groups')}),
    #     ('date', {'fields': ('date_joined', 'last_login', 'entry_date', 'official_date', 'resign_date')}),
    # )
    list_display = ('name', 'node', 'parent')
    search_fields = ['name', 'node', ]

admin.site.register(Tree, TreeAdmin)