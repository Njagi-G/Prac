from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# SQLAlchemy User Model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_picture = db.Column(db.String(120), default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

# Flask routes for user management
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'API is working!'})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if request.user.id != user_id:
        return jsonify({'error': 'You are not allowed to update this user'}), 403

    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        if request.json.get('password'):
            if len(request.json['password']) < 6:
                return jsonify({'error': 'Password must be at least 6 characters'}), 400
            user.password = bcrypt.hashpw(request.json['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        if request.json.get('username'):
            username = request.json['username']
            if len(username) < 7 or len(username) > 20:
                return jsonify({'error': 'Username must be between 7 and 20 characters'}), 400
            if ' ' in username:
                return jsonify({'error': 'Username cannot contain spaces'}), 400
            if username != username.lower():
                return jsonify({'error': 'Username must be lowercase'}), 400
            if not username.isalnum():
                return jsonify({'error': 'Username can only contain letters and numbers'}), 400
            user.username = username

        user.email = request.json.get('email', user.email)
        user.profile_picture = request.json.get('profilePicture', user.profile_picture)

        db.session.commit()

        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'profilePicture': user.profile_picture,
            'isAdmin': user.is_admin,
            'createdAt': user.created_at,
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not request.user.is_admin and request.user.id != user_id:
        return jsonify({'error': 'You are not allowed to delete this user'}), 403

    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User has been deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/signout', methods=['POST'])
def signout():
    try:
        return jsonify({'message': 'User has been signed out'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    if not request.user.is_admin:
        return jsonify({'error': 'You are not allowed to see all users'}), 403

    try:
        start_index = int(request.args.get('startIndex', 0))
        limit = int(request.args.get('limit', 9))
        sort_direction = 1 if request.args.get('sort') == 'asc' else -1

        users = User.query.order_by(User.created_at.desc()).offset(start_index).limit(limit).all()
        total_users = User.query.count()

        now = datetime.utcnow()
        one_month_ago = now - timedelta(days=30)
        last_month_users = User.query.filter(User.created_at >= one_month_ago).count()

        users_without_password = [{'id': user.id, 'username': user.username, 'email': user.email,
                                   'profilePicture': user.profile_picture, 'isAdmin': user.is_admin,
                                   'createdAt': user.created_at} for user in users]

        return jsonify({
            'users': users_without_password,
            'totalUsers': total_users,
            'lastMonthUsers': last_month_users,
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'profilePicture': user.profile_picture,
            'isAdmin': user.is_admin,
            'createdAt': user.created_at,
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
