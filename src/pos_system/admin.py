from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django_admin_inline_paginator.admin import TabularInlinePaginated
from . import models
from unfold import admin as unfold_admin



class ModelAdmin(unfold_admin.ModelAdmin):
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        if hasattr(qs.model, "company"):
            return qs.filter(company=request.user.company)
        return qs
    
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if hasattr(obj, "company"):
            obj.company = request.user.company
        return super().save_model(request, obj, form, change)



@admin.register(models.Consumer)
class ConsumerAdmin(ModelAdmin):
    pass



@admin.register(models.Product)
class ProductAdmin(ModelAdmin):
    pass
    # readonly_fields = ("stock_qty",)


@admin.register(models.Category)
class CategoryAdmin(ModelAdmin):
    search_fields = ("name",)


class OrderProductInline(TabularInlinePaginated):
    model = models.OrderProduct
    extra = 0
    
    # def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
    #     if obj:
    #         return ("product", "qty", "original_price", "price")
    #     return super().get_readonly_fields(request, obj)
    

@admin.register(models.Order)
class OrderAdmin(ModelAdmin):
    inlines = (OrderProductInline,)
    
    def changeform_view(self, request: HttpRequest, object_id: str | None = None, form_url: str = "", extra_context: unfold_admin.Dict[str, bool] | None = None) -> Any:
        extra_context = extra_context or dict()
        from pos_system_core.unfold import dashboard_callback
        extra_context = dashboard_callback(request, extra_context)
        extra_context["products"] = models.Product.objects.all()
        return super().changeform_view(request, object_id, form_url, extra_context)


@admin.register(models.Unit)
class UnitAdmin(ModelAdmin):
    pass
