from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# SQLAlchemy Comment Model
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.ARRAY(db.Integer), default=[])
    number_of_likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Comment {self.id} - Post ID: {self.post_id}>'

# Flask routes for comment management
@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    content = data.get('content')
    post_id = data.get('postId')
    user_id = data.get('userId')

    if not content or not post_id or not user_id:
        return jsonify({'error': 'All fields are required'}), 400

    new_comment = Comment(
        content=content,
        post_id=post_id,
        user_id=user_id,
    )

    try:
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/comments/<int:post_id>', methods=['GET'])
def get_post_comments(post_id):
    try:
        comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
        return jsonify(comments), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/comments/<int:comment_id>/like', methods=['PUT'])
def like_comment(comment_id):
    try:
        comment = Comment.query.get(comment_id)

        if not comment:
            return jsonify({'error': 'Comment not found'}), 404

        user_id = request.json.get('userId')

        if user_id not in comment.likes:
            comment.number_of_likes += 1
            comment.likes.append(user_id)
        else:
            comment.number_of_likes -= 1
            comment.likes.remove(user_id)

        db.session.commit()
        return jsonify(comment), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/comments/<int:comment_id>', methods=['PUT'])
def edit_comment(comment_id):
    try:
        comment = Comment.query.get(comment_id)

        if not comment:
            return jsonify({'error': 'Comment not found'}), 404

        user_id = request.json.get('userId')

        if comment.user_id != user_id:
            return jsonify({'error': 'You are not allowed to edit this comment'}), 403

        comment.content = request.json.get('content')
        db.session.commit()

        return jsonify(comment), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    try:
        comment = Comment.query.get(comment_id)

        if not comment:
            return jsonify({'error': 'Comment not found'}), 404

        user_id = request.json.get('userId')

        if comment.user_id != user_id:
            return jsonify({'error': 'You are not allowed to delete this comment'}), 403

        db.session.delete(comment)
        db.session.commit()

        return jsonify({'message': 'Comment has been deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/comments', methods=['GET'])
def get_comments():
    try:
        if not request.user.is_admin:
            return jsonify({'error': 'You are not allowed to get all comments'}), 403

        start_index = int(request.args.get('startIndex', 0))
        limit = int(request.args.get('limit', 9))
        sort_direction = -1 if request.args.get('sort') == 'desc' else 1

        comments = Comment.query.order_by(Comment.created_at.desc()).offset(start_index).limit(limit).all()
        total_comments = Comment.query.count()
        
        now = datetime.utcnow()
        one_month_ago = now - timedelta(days=30)
        last_month_comments = Comment.query.filter(Comment.created_at >= one_month_ago).count()

        return jsonify({
            'comments': [comment for comment in comments],
            'totalComments': total_comments,
            'lastMonthComments': last_month_comments
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
