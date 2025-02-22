import json

from redis import Redis


redis_client = Redis(host="redis", port=6379, db=0)


def cache_product(product_id: int, product_info: dict, ttl=3600):
    redis_client.set(f"product:{product_id}", json.dumps(product_info), ex=ttl)


def get_cached_product(product_id: int):
    if product_info := redis_client.get(f"product:{product_id}"):
        return json.loads(product_info)

    return None
