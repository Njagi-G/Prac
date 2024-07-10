from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key for JWT
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)  # JWT expiration time

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# SQLAlchemy User Model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'

# Flask routes for authentication
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Signup successful'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid password'}), 400

    token = jwt.encode({
        'id': user.id,
        'isAdmin': user.is_admin,
        'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
    }, app.config['SECRET_KEY'])

    response = make_response(jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'profile_picture': user.profile_picture,
        'is_admin': user.is_admin,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    }), 200)
    response.set_cookie('access_token', token, httponly=True)

    return response

@app.route('/google', methods=['POST'])
def google():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    google_photo_url = data.get('googlePhotoUrl')

    try:
        user = User.query.filter_by(email=email).first()

        if user:
            token = jwt.encode({
                'id': user.id,
                'isAdmin': user.is_admin,
                'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
            }, app.config['SECRET_KEY'])

            response = make_response(jsonify({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile_picture': user.profile_picture,
                'is_admin': user.is_admin,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }), 200)
            response.set_cookie('access_token', token, httponly=True)

            return response
        else:
            generated_password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            hashed_password = bcrypt.generate_password_hash(generated_password).decode('utf-8')

            new_user = User(
                username=name.lower().replace(' ', '') + ''.join(random.choices(string.digits, k=4)),
                email=email,
                password=hashed_password,
                profile_picture=google_photo_url,
            )

            db.session.add(new_user)
            db.session.commit()

            token = jwt.encode({
                'id': new_user.id,
                'isAdmin': new_user.is_admin,
                'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
            }, app.config['SECRET_KEY'])

            response = make_response(jsonify({
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'profile_picture': new_user.profile_picture,
                'is_admin': new_user.is_admin,
                'created_at': new_user.created_at,
                'updated_at': new_user.updated_at
            }), 200)
            response.set_cookie('access_token', token, httponly=True)

            return response
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Run the Flask application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
