from core import *
from instance.models import *

from flask import request
from werkzeug.utils import secure_filename
import os


@application.route('/addPizzas', methods=["PUT"])
@jwt_required()
def putItem():
    name = get_jwt()['sub']
    try:
        pizza_id = request.json.get("pizza_id")
        count = request.json.get('count')
    except:
        resp = {
            "errCode": 1,
            "errString": "нехватает данных"
        }
        return resp, 401
    
    # Получение пользователя по имени
    user = User.query.filter_by(name=name).first()
    if not user:
        resp = {
            "errCode": 2,
            "errString": "пользователь не найден"
        }
        return resp, 404
    
    # Проверяем, существует ли пицца с указанным id
    pizza = Pizzas.query.get(pizza_id)
    if not pizza:
        resp = {
            "errCode": 3,
            "errString": "пицца не найдена"
        }
        return resp, 404
    
    # Создание новой записи в корзине
    new_item = Cart(user_id=user.id, pizza_id=pizza_id, count=count)
    db.session.add(new_item)
    db.session.commit()
    
    resp = {
        "success": True,
        "message": "Пицца успешно добавлена в корзину"
    }
    return resp, 200

@application.route('/addItemAdmin', methods=['POST'])
def add_item():
    try:
        # Получение данных из запроса
        data = request.form
        name = data.get('name')
        sizes = ','.join(data.getlist('sizes'))  # Преобразование в строку
        types = ','.join(data.getlist('type'))  # Преобразование в строку
        price = data.get('price')
        rating = data.get('rating')
        category = data.get('category')
        imageURL = data.get('imageURL')
        imageFile = request.files.get('image')

        # Проверка на наличие изображения
        if imageFile and imageFile.filename != '':
            # Генерация уникального имени файла
            filename = secure_filename(imageFile.filename)
            unique_filename = f"{category}_{filename}"
            upload_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../front/public/assets/img/pizzas'))
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            path = os.path.join(upload_folder, unique_filename)
            imageFile.save(path)

            # Формирование ссылки на сохраненное изображение
            imageURL = f"/assets/img/pizzas/{unique_filename}"

        if not imageURL:
            return jsonify({"error": "Image URL or file is required"}), 400

        # Сохранение данных о пицце в базу данных
        pizza = Pizzas(name=name, sizes=sizes, types=types, price=price, rating=rating, category=category, imageURl=imageURL)
        db.session.add(pizza)
        db.session.commit()

        # Отправка ответа об успешном добавлении пиццы
        return jsonify({"message": "Пицца успешно добавлена", "data": {
            "name": name,
            "sizes": sizes.split(','),  # Преобразование обратно в список
            "type": types.split(','),  # Преобразование обратно в список
            "price": price,
            "rating": rating,
            "category": category,
            "imageURL": imageURL
        }}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500