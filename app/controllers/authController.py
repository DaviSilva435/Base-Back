from app 				import app, db, Messages
from flask 				import request, jsonify
from flask_jwt_extended	import jwt_required, create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
from sqlalchemy 		import exc

from app import User
from app import AuthValidator

#--------------------------------------------------------------------------------------------------#

@app.route('/auth', methods=['POST'])
def login():
	data = request.get_json()

	validator = AuthValidator(data)
	errors = validator.validate()

	if(errors['has']):
		return jsonify({'message': Messages.FORM_VALIDATION_ERROR, 'error': errors['has'], 'errors': errors}), 200

	user = User.query.filter(User.username == data['username']).first()

	return jsonify({
        'access_token': create_access_token(identity=user.id),
        'refresh_token': create_refresh_token(identity=user.id),
        'user_role': user.role_id
    }), 200

#--------------------------------------------------------------------------------------------------#

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    
    return jsonify({
        'access_token': create_access_token(identity=current_user)
    }), 200

#--------------------------------------------------------------------------------------------------#

@app.route('/me', methods=['GET'])
@jwt_required
def me():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    return jsonify({
        'username': user.username,
        'email': user.email,
        'role_id': user.role_id,
        'role': {
        	'id': user.roles.id,
        	'name': user.roles.name
        }
    }), 200

#--------------------------------------------------------------------------------------------------#