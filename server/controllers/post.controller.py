from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# SQLAlchemy Post Model
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String, default='https://www.hostinger.com/tutorials/wp-content/uploads/sites/2/2021/09/how-to-write-a-blog-post.png')
    category = db.Column(db.String, default='uncategorized')
    slug = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.id} - Title: {self.title}>'

# Flask routes for post management
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    if not request.user.is_admin:
        return jsonify({'error': 'You are not allowed to create a post'}), 403
    if not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Please provide all required fields'}), 400

    slug = data.get('title').lower().replace(' ', '-').replace('-', '')
    new_post = Post(
        title=data.get('title'),
        content=data.get('content'),
        image=data.get('image', 'https://www.hostinger.com/tutorials/wp-content/uploads/sites/2/2021/09/how-to-write-a-blog-post.png'),
        category=data.get('category', 'uncategorized'),
        slug=slug,
        user_id=request.user.id
    )

    try:
        db.session.add(new_post)
        db.session.commit()
        return jsonify(new_post), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/posts', methods=['GET'])
def get_posts():
    try:
        start_index = int(request.args.get('startIndex', 0))
        limit = int(request.args.get('limit', 9))
        sort_direction = 1 if request.args.get('order') == 'asc' else -1

        filters = {}
        if request.args.get('userId'):
            filters['user_id'] = request.args.get('userId')
        if request.args.get('category'):
            filters['category'] = request.args.get('category')
        if request.args.get('slug'):
            filters['slug'] = request.args.get('slug')
        if request.args.get('postId'):
            filters['_id'] = request.args.get('postId')
        if request.args.get('searchTerm'):
            filters['$or'] = [
                {'title': {'$regex': request.args.get('searchTerm'), '$options': 'i'}},
                {'content': {'$regex': request.args.get('searchTerm'), '$options': 'i'}}
            ]

        posts = Post.query.filter_by(**filters).order_by(Post.updated_at.desc()).offset(start_index).limit(limit).all()
        total_posts = Post.query.count()

        now = datetime.utcnow()
        one_month_ago = now - timedelta(days=30)
        last_month_posts = Post.query.filter(Post.created_at >= one_month_ago).count()

        return jsonify({
            'posts': [post for post in posts],
            'totalPosts': total_posts,
            'lastMonthPosts': last_month_posts,
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        post = Post.query.get(post_id)

        if not post:
            return jsonify({'error': 'Post not found'}), 404

        if not request.user.is_admin or request.user.id != post.user_id:
            return jsonify({'error': 'You are not allowed to delete this post'}), 403

        db.session.delete(post)
        db.session.commit()

        return jsonify({'message': 'The post has been deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        post = Post.query.get(post_id)

        if not post:
            return jsonify({'error': 'Post not found'}), 404

        if not request.user.is_admin or request.user.id != post.user_id:
            return jsonify({'error': 'You are not allowed to update this post'}), 403

        post.title = request.json.get('title', post.title)
        post.content = request.json.get('content', post.content)
        post.category = request.json.get('category', post.category)
        post.image = request.json.get('image', post.image)

        db.session.commit()

        return jsonify(post), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Run the Flask application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
