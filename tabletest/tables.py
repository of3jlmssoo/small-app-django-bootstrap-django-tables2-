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

class NumberColumn(tables.Column):
    def render(self, value):
        return '{:0.0f}'.format(value)


class Bootstrap4Table(tables.Table):
    id = tables.Column(linkify=True)
    goods = tables.Column(attrs={
        # "th": {"align": "justify"},
        # "td": {"align": "center"},
        # "th": {"align": "center"},
    })
    alternative = tables.columns.BooleanColumn(yesno='有,無')
    updated_on = tables.columns.DateColumn(short=True)

    # product_price = tables.Column()
    product_price = NumberColumn(
        attrs={
            "td": {"align": "right"}
        }
    )

    # country = tables.Column(linkify=True)
    # continent = tables.Column(accessor="country__continent", linkify=True)

    class Meta:
        model = ProductOrder    # .objects.filter(product_type='D')
        template_name = "tabletest/bootstrap4.html"
        attrs = {"class": "table table-hover table-sm"}
        exclude = ("created_on","status","comment",)
        # exclude = ("friendly",)

    # def render_number(self, value):
    #     return '{:0.0f}'.format(value)
