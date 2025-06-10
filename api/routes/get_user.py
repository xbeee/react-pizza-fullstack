from core import *
from instance.models import *

@application.route('/users', methods=["GET"])
# @jwt_required()
def get_users():
    # current_user_email = get_jwt_identity()
    # user = User.query.filter_by(email=current_user_email).first()
    # if not user:
    #     return jsonify({'error': 'User not found'}), 404
    # if user.role != 'admin':
    #     return jsonify({'error': 'Unauthorized access'}), 403

    users = User.query.all()
    users_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'email': user.email,
            'Fsp': user.Fsp,
            'number': user.number
        }
        users_list.append(user_data)
    return jsonify(users_list)

@application.route('/get_user', methods=['GET'])
@jwt_required()
def get_admin():
    try:
        user_identity = get_jwt_identity()
        user = User.query.filter_by(email=user_identity).first()
        
        if user:
            if(user.role == 'admin'):
                print(user.role)
                return jsonify({"is_admin": 'true'}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500