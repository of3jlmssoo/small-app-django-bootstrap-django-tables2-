import django_tables2 as tables

from .models import ProductOrder



# class BootstrapTable(tables.Table):
#     class Meta:
#         model = ProductOrder
#         template_name = "tabletest/bootstrap.html"
#         fields = ("goods", "product_price", "type_of_estimation", "product_type", "product_use","alternative", "expected_purchase_date")
#         # linkify = ("goods")


# class ProductOrderTable(tables.Table):
#     name = tables.Column()
#     population = tables.Column()
#     tz = tables.Column(verbose_name="time zone")
#     visits = tables.Column()
#     summary = tables.Column(order_by=("name", "population"))

#     class Meta:
#         model = ProductOrder



class Bootstrap4Table(tables.Table):
    id = tables.Column(linkify=True)
    # country = tables.Column(linkify=True)
    # continent = tables.Column(accessor="country__continent", linkify=True)

    class Meta:
        model = ProductOrder
        template_name = "tabletest/bootstrap4.html"
        attrs = {"class": "table table-hover table-sm"}
        # exclude = ("friendly",)
