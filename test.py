#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 19:50:30 2022

@author: growth358
"""

import os
os.environ['FLASK_APP'] = 'project/__init__.py'
os.environ['APP_FOLDER'] = '.'
os.environ['FLASK_ENV'] = 'development'
os.environ['APP_SETTINGS']='src.config.DevelopmentConfig'
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@172.19.0.3:5432/api_dev'
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.api.models import Post,User
from flask_restx import Resource, Api, fields,marshal
import json
#instantiate the db
db = SQLAlchemy()  
#instantiate the app
app = Flask(__name__)

api = Api(app)
#set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

#set up extension
#set up db 
db.init_app(app)
app.app_context().push()

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
