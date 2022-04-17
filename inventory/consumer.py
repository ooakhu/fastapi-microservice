import sys
sys.path.insert(0, '/home/valerie/PycharmProjects/Micro-Service/') #had to add a path to this folder so that tthe script could see the redis on the payment folder
from inventory_main import Product, redis
# from payment.payment_main import redis, Order
import time

key = 'order_completed'
group = 'inventory-group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                    print(product.quantity, 'HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
                except:
                    redis.xadd('refund_order', obj, '*')
        print(results)


    except Exception as e:
        print(str(e))
    time.sleep(1)