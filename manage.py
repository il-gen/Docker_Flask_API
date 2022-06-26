#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from flask.cli import FlaskGroup
from src import create_app, db
from src.api.models import User, Post
from datetime import datetime, timedelta

app = create_app() #used at pytest
cli = FlaskGroup(create_app=create_app)
def drop_everything(db):
    """(On a live db) drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """
    import sqlalchemy
    from sqlalchemy.schema import DropConstraint, DropTable, MetaData, Table

    con = db.engine.connect()
    trans = con.begin()
    inspector = sqlalchemy.inspect(db.engine)

    # We need to re-create a minimal metadata with only the required things to
    # successfully emit drop constraints and tables commands for postgres (based
    # on the actual schema of the running instance)
    meta = MetaData()
    tables = []
    all_fkeys = []

    for table_name in inspector.get_table_names():
        fkeys = []

        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey["name"]:
                continue

            fkeys.append(db.ForeignKeyConstraint((), (), name=fkey["name"]))

        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)

    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))

    for table in tables:
        con.execute(DropTable(table))

    trans.commit()
    
    
@cli.command('recreate_db')
def recreate_db():
    drop_everything(db)
    db.drop_all()
    db.create_all()
    db.session.commit()
@cli.command('seed_db')
def seed_db():
    delta=datetime.now()
    user1 = User(username='User1', full_name='User1_fullname', email='User1@test.com',created_at=delta)
    user1.set_password("a")
    db.session.add(user1)
    
    delta=datetime.now() + timedelta(days=1)
    user2 = User(username='User2', full_name='User2_fullname', email='User2@test.com', created_at=delta)
    user2.set_password("b")
    db.session.add(user2)
    
    delta=datetime.now() + timedelta(days=2)
    user3 = User(username='User3', full_name='User3_fullname', email='User3@test.com', created_at=delta)
    user3.set_password("c")
    db.session.add(user3)
    
    delta=datetime.now() + timedelta(days=3)
    user4 = User(username='User4', full_name='User4_fullname', email='User4@test.com', created_at=delta)
    user4.set_password("d")
    db.session.add(user4)
    
    delta=datetime.now() + timedelta(days=4)
    post1 = Post(description="post1", owner=user1, created_at=delta)
    db.session.add(post1)
    
    delta=datetime.now() + timedelta(days=5)
    post2 = Post(description="post2", owner=user1, created_at=delta)
    db.session.add(post2)
    
    delta=datetime.now() + timedelta(days=6)
    post3 = Post(description="post3", owner=user1, created_at=delta)
    db.session.add(post3)
    
    delta=datetime.now() + timedelta(days=13)
    post4 = Post(description="post4", owner=user2, created_at=delta)
    db.session.add(post4)
    
    delta=datetime.now() + timedelta(days=12)
    post5 = Post(description="post5", owner=user2, created_at=delta)
    db.session.add(post5)
    
    delta=datetime.now() + timedelta(days=9)
    post6 = Post(description="post6", owner=user3, created_at=delta)
    db.session.add(post6)
    
    delta=datetime.now() + timedelta(days=10)
    post7 = Post(description="post7", owner=user4, created_at=delta)
    db.session.add(post7)
    
    delta=datetime.now() + timedelta(days=10)
    post8 = Post(description="post8", owner=user4, created_at=delta)
    db.session.add(post8)
    
    user1.like_post(post1)
    user1.like_post(post3)
    user1.like_post(post5)
    user2.like_post(post2)
    user2.like_post(post4)
    user4.like_post(post1)
    user4.like_post(post2)
    user1.follow_user(user3)
    user1.follow_user(user4)
    user2.follow_user(user1)
    user2.follow_user(user4)
    db.session.commit()
    
    
    
if __name__ == '__main__':
    cli()
