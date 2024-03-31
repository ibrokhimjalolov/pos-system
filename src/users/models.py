from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _



class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        db_table = "companies"


class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="users", null=True, blank=True)
    
    class UserRole(models.TextChoices):
        OWNER = "owner", _("Owner")
        COURIER = "courier", _("Courier")
        
    role = models.CharField(max_length=255, null=True, blank=True, choices=UserRole.choices)



class Employee(User):
    class Meta:
        proxy = True
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")
