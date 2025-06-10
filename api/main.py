from core import *
import auth
from instance.models import Pizzas, User
import routes.getPizza
import routes.get_requset
import routes.get_user
import putRequest.putItem
import putRequest.putCart
import putRequest.putOrder
import json
import sys
import os

with application.app_context():
    db.create_all()
    def СreateMap():
        from instance.models import Pizzas
        script_dir = os.path.dirname(sys.argv[0])
        with open(os.path.join(script_dir, 'instance/pizzas.json'), 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        for el in data:
            category = el['category']
            imageURl = el['imageURl']
            name = el['name']
            price = el['price']
            rating = el['rating']
            sizes = el['sizes']
            types = el['types']
            row = Pizzas(types=types, sizes=sizes, rating=rating, price=price, name=name, imageURl=imageURl, category=category)
   
            db.session.add(row)
        admin_email = "adminreact@yandex.ru"
        admin_password = "AdminReact"
        admin_hashed_password = generate_password_hash(admin_password)
        admin_number = 0
        admin_role = "admin"
        admin_Fsp = "admin"
        
        admin_user = User(email=admin_email, password=admin_hashed_password, number=admin_number, role=admin_role, Fsp=admin_Fsp)
        db.session.add(admin_user)
        db.session.commit()
    СreateMap()

if __name__ == '__main__':
    application.run(debug=True)