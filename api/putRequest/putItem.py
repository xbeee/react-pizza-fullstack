from core import *
from instance.models import *
from werkzeug.utils import secure_filename
from flask import request
from sqlalchemy import text
import sys
import os
sys.path.append('../')
# изменение пиццы в админке
@application.route('/editPizza/<int:pizza_id>', methods=['PUT'])
def edit_pizza(pizza_id):
  
    try:
        # Получение данных из запроса
        data = request.form
        name = data.get('name')
        sizes = data.get('sizes')
        category = data.get('category')
        types = data.get('types')
        rating = data.get('rating')
        price = data.get('price')
        imageURL = data.get('imageURL')
        imageFile = request.files.get('imageFile')

        # Поиск пиццы в базе данных по ID
        pizza = Pizzas.query.get(pizza_id)

        if not pizza:
            return jsonify({"error": "Pizza not found"}), 404

        # Обработка загрузки изображения
        if imageURL == '':
            # Генерация уникального имени файла
            filename = secure_filename(imageFile.filename)
            unique_filename = f"{pizza_id}_{filename}"
            path = '../front/public/assets/img/pizzas/' + imageFile.filename
            imageFile.save(path)
            os.rename(path, '../front/pubic/assets/img/pizzas/'+ unique_filename)
            # path = '../../front/src/assets/img/pizzas/' + imageFile.filename
            # imageFile.save(path)
            # os.rename(path, '../../front/src/assets/img/pizzas/'+ unique_filename)

            # Сохранение изображения на сервере

            # Формирование ссылки на сохраненное изображение
            imageURL = f"/assets/src/img/pizzas/{unique_filename}"  # Расширение jpg для примера

        # Обновление данных пиццы в базе данных
        pizza.name = name
        pizza.sizes = sizes
        pizza.types = types
        pizza.price = price
        pizza.imageURl = imageURL
        pizza.category = category
        pizza.rating = rating

        # Сохранение изменений в базе данных
        db.session.commit()

        # Возвращение успешного ответа
        return jsonify({"message": "Pizza updated successfully", "imageURL": imageURL}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@application.route('/deletePizza/<int:pizza_id>', methods=['DELETE'])
def delete_pizza(pizza_id):
    try:
        pizza = Pizzas.query.filter_by(id=pizza_id).first()

        if not pizza:
            return jsonify({"error": "Pizza not found"}), 404

        db.session.delete(pizza)
        db.session.commit()

        all_pizzas = Pizzas.query.order_by(Pizzas.id).all()
        for i, pizza in enumerate(all_pizzas):
            new_id = i + 1
            db.session.execute(text("UPDATE Pizzas SET id = :new_id WHERE id = :old_id"), {'new_id': new_id, 'old_id': pizza.id})

        db.session.commit()

        # Сброс автоинкремента для SQLite
        # db.session.execute(text("DELETE FROM sqlite_sequence WHERE name = 'Pizzas'"))
        # db.session.commit()

        return jsonify({"message": "Pizza deleted and IDs updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@application.route('/deleteUser/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        all_users = User.query.order_by(User.id).all()
        for i, user in enumerate(all_users):
            new_id = i + 1
            db.session.execute(text("UPDATE User SET id = :new_id WHERE id = :old_id"), {'new_id': new_id, 'old_id': user.id})

        db.session.commit()

        # Сброс автоинкремента для SQLite
        # db.session.execute(text("DELETE FROM sqlite_sequence WHERE name = 'User'"))
        # db.session.commit()

        return jsonify({"message": "User deleted and IDs updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500