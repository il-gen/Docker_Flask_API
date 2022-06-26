#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:27:19 2022

@author: growth358
"""
import os

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my_precious'

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL') 

class ProductionConfig(BaseConfig):
    url = os.environ.get('DATABASE_URL')
    if url is not None and url.startswith("postgres://"):
        url.replace("postgres://","postgresql://",1)
    SQLALCHEMY_DATABASE_URI = url