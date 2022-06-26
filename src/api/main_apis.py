#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 11:58:13 2022

@author: growth358
"""

from flask import Blueprint, request
from flask_restx import Resource, Api, fields, marshal

from src import db
from src.api.models import User,Post
from src.api.functions import LinkedList, mergeSort
import json


main_apis_blueprint = Blueprint('main_apis',__name__)
api = Api(main_apis_blueprint)

user_model = api.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True),
    'full_name': fields.String(required=True),
    'profile_picture': fields.String(required=True),
})

post_model = api.model('Post', {
    'id': fields.Integer(readOnly=True),
    'description': fields.String(required=True),
    'owner' :  fields.Nested(user_model),
    'image': fields.String(required=True),
    'created_at': fields.DateTime,
})

posts_model = api.model('Post', {
    'id': fields.Integer(readOnly=True),
    'description': fields.String(required=True),
    'image': fields.String(required=True),
    'created_at': fields.DateTime,
})

class UsersList(Resource):
    
    @api.marshal_with(user_model, as_list=True)
    def get(self):
        return User.query.all(), 200
    @api.expect(user_model, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get('username')
        email = post_data.get('email')
        response_object = {}
        
        user = User.query.filter_by(email=email).first()
        if user:
            response_object['message']= 'Sorry. That email already exists.'
            return response_object, 400
        
        db.session.add(User(username=username,email=email))
        db.session.commit()

        response_object['message'] = f'{email} was added!'
        return response_object, 201
    
class Users(Resource):
    
    @api.marshal_with(user_model)
    def get(self,user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(code=404, message=f"User {user_id} does not exist")
        return user, 200

class PostsList(Resource):
    
    @api.marshal_with(posts_model, as_list=True)
    def get(self):
        return Post.query.all(), 200
    
    
    
    
def get_posts(user_id,post_ids):
    posts=[]
    user=User.query.filter_by(id=user_id).first()
    if user:
        for i in post_ids:
            post=Post.query.filter_by(id=i).first()
            post_dic={}
            if post:                 
                post_dic = marshal(post,post_model)
                post_dic["liked"]=post.has_liked_by(user)
                post_dic["owner"]["fallowed"]=post.owner.has_followed_user(user)
                posts.append(post_dic)
            else:
                post_dic['id']=i
                post_dic['description']=None
                post_dic['owner' ]=None
                post_dic['image']=None
                post_dic['created_at']=None
                posts.append(post_dic)
    return posts

class getPosts(Resource):
    def post(self):
        post_data = request.get_json()
        user_id = post_data.get('user_id')
        post_ids = post_data.get('post_ids')
        
        posts=get_posts(user_id,post_ids)
        return posts

class mergePosts(Resource):
    def post(self):
        post_data = request.get_json()
        list_of_posts = post_data.get('list_of_posts')
        
        node_list=[]
        for posts in list_of_posts:
            #Let Convert list_of_posts into LinkList
            ll=LinkedList()    
            for post in posts:
                ll.insert(**post)
            #After finish every member of list_of_posts store heads 
            node_list.append(ll.head)
        #Let begin merge and sort 
        ms=mergeSort()
        # Merge all lists into one
        head = ms.mergeKLists(node_list)
        #Convert back Linklist to standard list using by reversed order
        ms.makeMList(head)
        return ms.ll

api.add_resource(UsersList, '/users')
api.add_resource(PostsList, '/posts')
api.add_resource(getPosts, '/get_posts')
api.add_resource(mergePosts, '/merge_posts')