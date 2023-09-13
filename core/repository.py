import logging
from .models import Product, Category
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger("info")


class ProductRepository:
    @staticmethod
    def get_products_by_category_name_without_time_create_and_time_update(category_name: str) -> QuerySet:
        return Product.objects.filter(category__name=category_name)\
            .select_related("category").only("name", "description", "quantity", "price", "category__name")

    @staticmethod
    def get_product_by_id(product_id: int) -> Product or None:
        try:
            return Product.objects.get(pk=product_id)
        except ObjectDoesNotExist as e:
            logger.warning(e)

    @staticmethod
    def decrement_product_quantity(product_id: int) -> bool:
        try:
            product = Product.objects.filter(pk=product_id).only("id", "quantity")
        except ObjectDoesNotExist as e:
            logger.warning(e)
        
        if product is not None:
            new_quantity = product.first().quantity - 1
            product.update(quantity=new_quantity)
            return True

        else:
            return False
