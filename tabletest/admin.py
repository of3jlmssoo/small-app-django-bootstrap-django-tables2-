from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import ProductOrder

# Register your models here.


class ProductOrderResource(resources.ModelResource):
    class Meta:
        model = ProductOrder

# class ProductOrderAdmin(admin.ModelAdmin):


class ProductOrderAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'goods',
        'product_price',
        'type_of_estimation',
        'product_type',
        'product_use',
        'alternative',
        'expected_purchase_date',
        'created_on',
        'updated_on',
    )
    list_display = (
        'id',
        'goods',
        'product_price',
        'type_of_estimation',
        'product_type',
        'product_use',
        'alternative',
        'status',
        'updated_on',
    )
    # list_display = (
    #     'id',
    #     'goods',
    #     'product_price',
    #     'type_of_estimation',
    #     'product_type',
    #     'product_use',
    #     'alternative',
    #     'status',
    #     'user',
    # )
    resource_class = ProductOrderResource


admin.site.register(ProductOrder, ProductOrderAdmin)
