from fastapi import FastAPI, status
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-18359.c55.eu-central-1-1.ec2.cloud.redislabs.com",
    port=18359,
    password="LpIdwtjrccpEqELdECYwbXvTBglbTJgF",
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get('/products') #@app because it is an endpoint
def all():
    return [format(pk) for pk in Product.all_pks()] #here we loop through all the items in product while calling the format function on them

def format(pk:str):
    product = Product.get(pk) #here we are getting the product that will be formated by pass the PK of the product

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)