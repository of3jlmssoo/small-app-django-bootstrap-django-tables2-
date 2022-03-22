from django.contrib import admin

# Register your models here.


from .models import ProductOrder

from import_export import resources
from import_export.admin import  ImportExportModelAdmin

class ProductOrderResource(resources.ModelResource):
    class Meta:
        model = ProductOrder

# class ProductOrderAdmin(admin.ModelAdmin):
class ProductOrderAdmin(ImportExportModelAdmin):
    list_display = ( 'id', 'goods', 'product_price', 'type_of_estimation', 'product_type', 'product_use', 'alternative', 'expected_purchase_date', 'created_on', 'updated_on',)
    resource_class=ProductOrderResource



admin.site.register(ProductOrder, ProductOrderAdmin)


