import django_tables2 as tables

from .models import ProductOrder


class NumberColumn(tables.Column):
    def render(self, value):
        return '{:0.0f}'.format(value)


class TruncatedTextColumn(tables.Column):
    def render(self, value):
        if len(value) > 10:
            return value[0:9] + '..'
        return str(value)


class Bootstrap4Table(tables.Table):

    id = tables.Column(linkify=True)
    goods = TruncatedTextColumn(accessor='goods')
    type_of_estimation = TruncatedTextColumn(accessor='type_of_estimation')

    alternative = tables.columns.BooleanColumn(yesno='有,無')
    updated_on = tables.columns.DateColumn(short=True)

    product_price = NumberColumn(
        attrs={
            "td": {"align": "right"}
        }
    )

    class Meta:
        model = ProductOrder    # .objects.filter(product_type='D')
        template_name = "tabletest/bootstrap4.html"
        attrs = {"class": "table table-hover table-sm"}
        exclude = ("created_on", "status", "comment",)
