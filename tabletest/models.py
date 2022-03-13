from django.db import models

# Create your models here.

from django.utils.translation import gettext_lazy as _

class ProductOrder(models.Model):

    class ProductType(models.TextChoices):
        DAILY = 'D', _('生活必需品')
        LUXURY = 'L', _('贅沢品')

    product_type = models.CharField(
        max_length=1,
        choices=ProductType.choices,
        default=ProductType.DAILY
    )

