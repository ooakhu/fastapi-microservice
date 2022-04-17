import sys

sys.path.insert(0, '/home/valerie/PycharmProjects/Micro-Service/')  # had to add a path to this folder so that tthe script could see the redis on the payment folder
from payment.payment_main import redis, Order
import time

key = 'refund_order'
group = 'payment-group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            print(results, 'resultttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj['pk'])
                order.status = 'order refunded'
                print("i get here at least")
                order.save()
                print(order, 'orederrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')


    except Exception as e:

        print(str(e))
    time.sleep(1)
