from instance.models import *
from core import *

@application.route('/login', methods=['POST'])
def Login():
    try:
        name = request.json.get('username')
        password = request.json.get('password')
    except:
        resp = {
            "errCode": 1,
            "errString": "нехватает данных"
        }
        return resp, 401

    user = User.query.filter_by(email=name).first()
    if user is None:
        resp = {
            "errCode": 2,
            "errString": "неверный логин"
        }
        return resp, 401
    if not check_password_hash(user.password, password):
        resp = {
            "errCode": 2,
            "errString": "неверный пароль"
        }
        return resp, 401
   
    token = create_access_token(identity=name)
    return {'access_token':token}

# выход из акаунта
@application.route('/logout', methods=["POST"])
def Logout():
    resp = jsonify({"msg":"logout successful"})
    unset_jwt_cookies(resp)
    return resp

@application.route('/register', methods=['POST'])
def Register():
    try:
        fullName = request.json.get('fullName') # Получение данных из формы
        email = request.json.get('email')
        password = request.json.get('password')
        phoneNumber = request.json.get('phoneNumber')
        role = 'user'
    except:
        resp = {
            "errCode": 1,
            "errString": "нехватает данных"
        }
        return resp, 401

    users = User.query.filter_by(email=email).first()
    if users:
        resp = {
            "errCode": 4,
            "errString": "такой пользователь уже есть"
        }
        return resp, 401
    password = generate_password_hash(password)

    user = User(email=email, password=password, number=phoneNumber, role=role, Fsp=fullName)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=email)
    return {'access_token':token}

