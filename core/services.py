import redis
import logging
import json
from djangoproject.settings import REDIS_HOST


logger = logging.getLogger("info")


class PaymentService:
    @staticmethod
    def get_line_item(
        name: str,
        description: str,
        price: float
    ) -> list:
        return [{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": name,
                    "description": description
                },
                "unit_amount": int(price),
            },
            "quantity": 1
        }]
    
    @staticmethod
    def register_product_buying_in_redis(product_id: int, user_id: int) -> bool:
        r = redis.Redis(REDIS_HOST, db=1)
        return r.set(name=str(user_id), value=json.dumps(str(product_id)))
    
    @staticmethod
    def get_product_buying_in_redis(user_id: int) -> str or None:
        r = redis.Redis(REDIS_HOST, db=1)
        product_id = r.get(name=str(user_id))
        return json.loads(product_id) if product_id is not None else None

    @staticmethod
    def delete_product_buying_in_redis(user_id: int) -> bool:
        r = redis.Redis(REDIS_HOST, db=1)
        return r.delete(str(user_id))
    