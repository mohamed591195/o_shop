import redis
from django.conf import settings
from .models import Product

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

class Recommender(object):

    def get_product_key(self, product_id):

        return f'product:{product_id}:purchased_with'

    def products_bought(self, products):

        products_ids = [p.id for p in products]

        for product_id in products_ids:

            for bought_with in products_ids:

                if bought_with != product_id:

                    r.zincrby(self.get_product_key(product_id), 1, bought_with)

    def suggest_products_for(self, products, max_results=6):

        products_ids = [p.id for p in products]

        if len(products_ids) == 1:

            suggestions = r.zrange(self.get_product_key(products_ids[0]), 0, -1, desc=True)[:max_results]
            print(suggestions)

        else:
            flat_ids = ''.join(str(id) for id in products_ids)
            tmp_key = f'tmp_{flat_ids}'

            products_keys = [self.get_product_key(id) for id in products_ids]

            r.zunionstore(tmp_key, *products_keys)

            r.zrem(tmp_key, *products_ids)

            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]

            r.delete(tmp_key)

        suggested_products_ids = [int(id) for id in suggestions]

        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))

        suggested_products.sort(key= lambda x: suggested_products_ids.index(x.id))

        return suggested_products

    def clear_purchases(self):

        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))

