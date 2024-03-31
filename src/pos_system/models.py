from django.db import models
from users.models import Company, User
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField



class BaseModel(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, editable=False)
    
    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = "category"
        
    def __str__(self) -> str:
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")
        db_table = "unit"
        
    def __str__(self) -> str:
        return self.name


    
class Product(BaseModel):
    is_active = models.BooleanField(default=True)

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True, default="")
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    count_in_box = models.PositiveIntegerField(null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    stock_qty = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, 
        verbose_name="Stock Quantity", editable=False
    )
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        db_table = "product"
        
    def __str__(self) -> str:
        return self.name


class Consumer(BaseModel):
    full_name = models.CharField(_("Full Name"), max_length=255)
    phone_number = PhoneNumberField(_("Phone Number"))
    address = models.TextField(_("Address"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Consumer")
        verbose_name_plural = _("Consumers")
        db_table = "consumer"
        
    def __str__(self) -> str:
        return self.full_name
    

class OrderStatus(models.TextChoices):
    CREATED = "created", _("Created")
    CANCELED = "canceled", _("Canceled")
    COMPLETED = "completed", _("Completed")    


class OrderQuerySet(models.QuerySet):
    pass


class Order(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    consumer = models.ForeignKey(Consumer, on_delete=models.PROTECT, null=True, blank=True)
    courier = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.CREATED)
    
    total_price: int  # will be annotated
    
    objects = OrderQuerySet.as_manager()
    
    
    def __str__(self) -> str:
        return str(self.pk)
    
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        db_table = "order"
    
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    
    qty = models.PositiveIntegerField()
    
    # pricing for single product
    original_price = models.PositiveIntegerField(editable=False)  # original price before discounts
    price = models.PositiveIntegerField(editable=False)  # price after discounts
    # end pricing
    
    
    def save(self, *args, **kwargs):
        if self.original_price is None:
            self.original_price = self.product.price
        if self.price is None:
            self.price = self.product.price
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _("Order Product")
        verbose_name_plural = _("Order Products")
        db_table = "order_product"
        
    def __str__(self) -> str:
        return f"{self.product.name} - {self.qty}x{self.price}"
