from app 				import app, db
from flask 				import request, jsonify
from flask_jwt 			import jwt_required
from werkzeug.security 	import generate_password_hash
from . 					import resource

from app.models.usersTable import User

@app.route('/user/all', methods=['GET'])
@jwt_required()
@resource('users-all')
def all():
	users = User.query.all()

	output = []

	for user in users:
		data = {}
		data['id'] 			= user.id
		data['username'] 	= user.username
		data['password'] 	= user.password
		output.append(data)

	return jsonify({'users': output})

@app.route('/user/view/<user_id>', methods=['GET'])
@jwt_required()
@resource('users-view')
def view(user_id):
	user = User.query.get(user_id)
	if not user:
		return jsonify({'message': 'No user found!'})

	data = {}
	data['id'] = user.id
	data['username'] = user.username
	data['password'] = user.password

	return jsonify({'user': data})


@app.route('/user/add', methods=['POST'])
@jwt_required()
@resource('users-add')
def add():
	data 			= request.get_json()
	hashed_pass     = generate_password_hash(data['password'], method='sha256')
	user 			= User(username=data['username'], password=hashed_pass, role_id=data['role_id'])
	db.session.add(user)
	db.session.commit()
	return jsonify({'message': 'New user created'})

@app.route('/user/edit/<user_id>', methods=['PUT'])
@jwt_required()
@resource('users-edit')
def edit(user_id):
	user = User.query.get(user_id)
	if not user:
		return jsonify({'message': 'No user found!'})

	data 		  = request.get_json()
	hashed_pass   = generate_password_hash(data['password'], method='sha256')
	user.username = data['username']
	user.password = hashed_pass

	db.session.commit()

	data = {}
	data['id'] 		 = user.id
	data['username'] = user.username
	data['password'] = user.password

	return jsonify(data)


@app.route('/user/delete/<user_id>', methods=['DELETE'])
@jwt_required()
@resource('users-delete')
def delete(user_id):
	user = User.query.get(user_id)
	if not user:
		return jsonify({'message': 'No user found!'})

	db.session.delete(user)
	db.session.commit()

	return jsonify({'message': "User has been deleted."})
