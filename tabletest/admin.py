from django.contrib import admin

# Register your models here.


from .models import ProductOrder

class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ( 'goods', 'product_price', 'type_of_estimation', 'product_type', 'product_use', 'alternative', 'expected_purchase_date', 'created_on', 'updated_on',)




admin.site.register(ProductOrder, ProductOrderAdmin)
