#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import jsonify, request
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Comment, Post

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'profile_picture': user.profile_picture,
        'is_admin': user.is_admin,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    } for user in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        profile_picture=data.get('profilePicture', 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'),
        is_admin=data.get('isAdmin', False)
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{
        'id': post.id,
        'user_id': post.user_id,
        'content': post.content,
        'title': post.title,
        'image': post.image,
        'category': post.category,
        'slug': post.slug,
        'created_at': post.created_at,
        'updated_at': post.updated_at
    } for post in posts])

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = Post(
        user_id=data['userId'],
        content=data['content'],
        title=data['title'],
        image=data.get('image', 'https://www.hostinger.com/tutorials/wp-content/uploads/sites/2/2021/09/how-to-write-a-blog-post.png'),
        category=data.get('category', 'uncategorized'),
        slug=data['slug']
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'}), 201

@app.route('/comments', methods=['GET'])
def get_comments():
    comments = Comment.query.all()
    return jsonify([{
        'id': comment.id,
        'content': comment.content,
        'post_id': comment.post_id,
        'user_id': comment.user_id,
        'likes': comment.likes,
        'number_of_likes': comment.number_of_likes,
        'created_at': comment.created_at,
        'updated_at': comment.updated_at
    } for comment in comments])

@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    new_comment = Comment(
        content=data['content'],
        post_id=data['post_id'],
        user_id=data['user_id']
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment created successfully'}), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)

