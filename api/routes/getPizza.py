from core import *
from instance.models import *

# вся пицца 
@application.route('/pizzas', methods=["GET"])
def GetPizza():
  pizzas = Pizzas.query.all()
  resp = []
  for el in pizzas:
    row = {
        'id': el.id,
        'name': el.name,
        'imageURL': el.imageURl,
        'price': el.price,
        'sizes': el.sizes,
        'price': el.price,
        'types': el.types,
        'category': el.category,
        'rating': el.rating
    }
    resp.append(row)
  return resp