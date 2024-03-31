from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company, Employee
from unfold import admin as unfold_admin


@admin.register(User)
class UserAdmin(UserAdmin, unfold_admin.ModelAdmin):
    fieldsets = None


@admin.register(Company)
class CompanyAdmin(unfold_admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(unfold_admin.ModelAdmin):
    pass
