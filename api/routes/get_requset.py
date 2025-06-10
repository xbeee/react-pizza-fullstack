from core import *
from instance.models import *


@application.route('/getUser', methods=["GET"])
@jwt_required()
def get_user():
    user_email = get_jwt()["sub"]
    print(user_email)
    
    # Проверяем, что пользователь существует
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return {
            "errCode": 404,
            "errString": "Пользователь не найден"
        }, 404
    
    # Возвращаем информацию о пользователе
    return {
        "id": user.id,
        "email": user.email,
        "Fsp": user.Fsp,
        "number": user.number
    }


@application.route('/editUser', methods=['POST'])
@jwt_required()
def edit_user():

    # Получение данных, которые пришли в теле запроса
  new_data = request.json  # Предполагается, что данные приходят в формате JSON
  print(new_data)
  current_user_email = get_jwt_identity()

  # Найдите пользователя в базе данных по электронной почте (или другому идентификатору) current_user_email
  user = User.query.filter_by(email=current_user_email).first()

  if not user:
    return {"error": "Пользователь не найден"}, 404

  updated_token = None  # Переменная для хранения обновленного токена

  # Обновление данных пользователя
  if 'Fsp' in new_data and new_data['Fsp'] != user.Fsp:
    user.Fsp = new_data['Fsp']
    print(1)
  if 'email' in new_data and new_data['email'] != current_user_email:
      # Обновление email в JWT токене
    user.email = new_data['email']
    updated_token = create_access_token(identity=new_data['email'])
    print(2)

  if 'number' in new_data and new_data['number'] != user.number:
      # Проверка уникальности номера телефона
    if User.query.filter_by(number=new_data['number']).first() and new_data['number'] != user.phone:
      return {"error": "Этот номер телефона уже используется другим пользователем"}, 400
    user.number = new_data['number']
    print(3)

  # Сохранение изменений в базе данных
  try:
    db.session.commit()
    return {"message": "Данные пользователя успешно обновлены", "token": updated_token}, 200
  except:
    db.session.rollback()
    return {"error": "Произошла ошибка при сохранении данных. Проверьте уникальность email и номера телефона."}, 400


@application.route('/getCart', methods=['GET'])
@jwt_required()
def get_cart():
    # Получение id пользователя из JWT
    user_email = get_jwt_identity()

    # Нахождение пользователя в базе данных по id
    user = User.query.filter_by(email=user_email).first()

    if not user:
        return {"error": "Пользователь не найден"}, 404

    # Получение всех товаров из корзины данного пользователя
    cart_items = Cart.query.filter_by(user_id=user.id).all()

    # Подготовка данных для ответа
    cart_data = []
    for item in cart_items:
        cart_data.append({
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "product_type": item.product_type,
            "product_name": item.product_name,
            "product_size": item.product_size,
            "price": item.price,
            "imageURL": item.imageURL,
        })

    return {"user_cart": cart_data}, 200


@application.route('/userOrders', methods=["GET"])
@jwt_required()
def get_user_orders():
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()

    if not current_user:
        return jsonify({'message': 'User not found'}), 404

    user_id = current_user.id
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.order_id).all()

    user_orders = {}
    for order in orders:
        if order.order_id not in user_orders:
            user_orders[order.order_id] = []
        user_orders[order.order_id].append({
            'product_id': order.product_id,
            'product_name': order.product_name,
            'user_id': order.user_id,
            'quantity': order.quantity,
            'price': order.price,
            'product_type': order.product_type,
            'product_size': order.product_size,
            'imageURL': order.imageURL
        })

    return jsonify({'orders': user_orders}), 200
  
@application.route('/deleteOrder/<string:order_id>', methods=['DELETE'])
def delete_order(order_id):
  try:
    orders_to_delete = Order.query.filter_by(order_id=order_id).all()
    for order in orders_to_delete:
      db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Orders deleted successfully'}), 200
  except Exception as e:
    db.session.rollback()
    return jsonify({'message': 'Failed to delete orders', 'error': str(e)}), 500


# @api.route('/changePassword', methods=['POST'])
# @jwt_required()
# def change_password():
#   current_user_email = get_jwt_identity()
#   new_password = request.json.get('newPassword')

#   # Проверяем, получено ли новое значение пароля
#   if not new_password:
#     return jsonify({'message': 'New password is required'}), 400

#   # Получаем пользователя из базы данных
#   user = User.query.filter_by(email=current_user_email).first()

#   # Проверяем, существует ли пользователь с указанным email
#   if not user:
#     return jsonify({'message': 'User not found'}), 404

#   # Генерируем хэш нового пароля
#   hashed_password = generate_password_hash(new_password)

#   # Сохраняем хэш нового пароля в базе данных
#   user.password = hashed_password
#   user.save()

#   return jsonify({'message': 'Password changed successfully'}), 200


