#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 10:34:17 2022

@author: growth358
"""

from flask import Blueprint
from flask_restx import Resource, Api


ping_blueprint = Blueprint('ping', __name__)
api = Api(ping_blueprint)

class Ping(Resource):
    def get(self):
        return {
            'status' : 'success',
            'message' : 'pong!'
            }
    
api.add_resource(Ping,'/ping')
    