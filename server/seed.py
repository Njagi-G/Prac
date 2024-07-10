#!/usr/bin/env python3

# Standard library imports
from random import choice as rc

# Remote library imports
from faker import Faker
from werkzeug.security import generate_password_hash

# Local imports
from app import app
from models import db, User, Post, Comment  # Import your models

fake = Faker()

def generate_random_password():
    return generate_password_hash('randompassword123')  # Use generate_password_hash to hash the password

def create_users(num):
    users = []
    for _ in range(num):
        password = generate_random_password()
        user = User(username=fake.user_name(), email=fake.email(), password=password)
        users.append(user)
        db.session.add(user)
    db.session.commit()
    return users

def create_posts(users, num):
    posts = []
    for _ in range(num):
        user = rc(users)
        title = fake.sentence()
        slug = generate_slug(title)  # Generate a unique slug based on the title
        post = Post(title=title, content=fake.text(), user_id=user.id, slug=slug)
        posts.append(post)
        db.session.add(post)
    db.session.commit()
    return posts

def generate_slug(title):
    # Convert title to lowercase and replace spaces with hyphens
    return title.lower().replace(' ', '-')


def create_comments(users, posts, num):
    for _ in range(num):
        user = rc(users)
        post = rc(posts)
        comment = Comment(content=fake.sentence(), user_id=user.id, post_id=post.id)
        db.session.add(comment)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")

        # Clear existing data
        db.session.query(Comment).delete()
        db.session.query(Post).delete()
        db.session.query(User).delete()

        # Create and add fake data
        users = create_users(10)
        posts = create_posts(users, 20)
        create_comments(users, posts, 50)

        print("Seeding complete!")
