#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 10:42:09 2022

@author: growth358
"""
from sqlalchemy.sql import func
from src import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    full_name = db.Column(db.String(100))
    profile_picture = db.Column(db.String(200), default="https://picture")
    bio = db.Column(db.String(200), default="about:")
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    password = db.Column(db.String(500))
    
 
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.id)
    
    
    liked_post = db.relationship('PostLike',
                            foreign_keys='PostLike.user_id',
                            backref='user_liked', lazy='dynamic')

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)
    
    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id,post_id=post.id).delete()
    
    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0
    
    followed = db.relationship('UserFollow',
                            foreign_keys='UserFollow.followed_id',
                            backref='user_followed', lazy='dynamic')
    
    follower = db.relationship('UserFollow',
                            foreign_keys='UserFollow.follower_id',
                            backref='user_follower', lazy='dynamic')

    def follow_user(self, user):
        if not self.has_followed_user(user):
            follow = UserFollow(followed_id=user.id, follower_id=self.id)
            db.session.add(follow)
    
    def unfollow_user(self, user):
        if self.has_followed_user(user):
            UserFollow.query.filter_by(followed_id=user.id, follower_id=self.id).delete()
    
    def has_followed_user(self, user):
        return UserFollow.query.filter(
            UserFollow.followed_id == self.id,
            UserFollow.follower_id == user.id).count() > 0 
    
    
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # primary keys are required by SQLAlchemy
    description = db.Column(db.String(100))
    image = db.Column(db.String(100), default="https://image")
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', foreign_keys="[Post.user_id]", backref=db.backref("posts", lazy="dynamic"))
    
    def __repr__(self):
        return f'<Post "{self.description[:20]}...">'
    
    liked_by = db.relationship('PostLike',
                            foreign_keys='PostLike.post_id',
                            backref='posts', lazy='dynamic')
    def has_liked_by(self, user):
        return PostLike.query.filter(
            PostLike.user_id == user.id,
            PostLike.post_id == self.id).count() > 0
    
    

    
class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    

class UserFollow(db.Model):
    __tablename__ = 'user_follow'
    # Let first user is followed, and second is follower
    id = db.Column(db.Integer, primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    

    