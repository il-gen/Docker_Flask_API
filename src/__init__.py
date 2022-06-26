#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



#instantiate the db
db = SQLAlchemy()   


def create_app(script_info=None):
    
    #instantiate the app
    app = Flask(__name__)
    
    #set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    #set up extension
    #set up db 
    db.init_app(app)
    
    #register blueprints
    
    from src.api.ping import ping_blueprint
    app.register_blueprint(ping_blueprint)
    
    from src.api.main_apis import main_apis_blueprint
    app.register_blueprint(main_apis_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app' : app, 'db' : db}
    
    return app
        



