from django.contrib import admin
from .models import Category, Product
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name',]
    search_fields = ['name',]
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','sku','category','price','stock','status','created_at',]
    list_filter = ['category','status',]
    search_fields = ['name','sku',]