from core import *
from instance.models import *


@application.route('/getCart', methods=["GET"])
@jwt_required()
def getuser():
  cart = Cart.query.all();
  resp = []
  for el in cart:
    row = {
        'id': el.id,
        'id_user': el.id_user,
        'id_pizza': el.id_pizza,
    }
    resp.append(row)
  return resp

# для отдельного пользователя