from django.db import models
from django.urls import reverse
# Create your models here.
from accounts.models import Account

from django.utils.translation import gettext_lazy as _

# class ProductOrder(models.Model):

#     class ProductType(models.TextChoices):
#         DAILY = 'D', _('生活必需品')
#         LUXURY = 'L', _('贅沢品')

#     product_type = models.CharField(
#         max_length=1,
#         choices=ProductType.choices,
#         default=ProductType.DAILY
#     )


class ProductOrder(models.Model):

    PRODUCT_TYPE = [
        ('D', '日常品'),
        ('L', '贅沢品'),
    ]
    PRODUCT_USE = [
        ('F', '家族用'),
        ('M', '自分用'),
        ('G', '贈答用'),
    ]

    # id(PK) djangoに任せる
    goods = models.CharField(max_length=50, blank=False, null=False)
    product_price = product_price = models.FloatField()
    type_of_estimation = models.CharField(max_length=50, blank=False, null=False)
    product_type = models.CharField(max_length=1, choices=PRODUCT_TYPE, blank=False, null=False)  # daily or luxury
    product_use = models.CharField(max_length=1, choices=PRODUCT_USE, blank=False, null=False)  # me, family or gift
    alternative = models.BooleanField()
    expected_purchase_date = models.DateField()

    # order_number =
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.goods


    def get_absolute_url(self):
        return reverse("productorder_detail", args=(self.pk,))
