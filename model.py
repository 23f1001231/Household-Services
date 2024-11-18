from flask_sqlalchemy import SQLAlchemy                                                                                   

db = SQLAlchemy()                                                                                                         

class users(db.Model):                                                                                                    
    __tablename__="customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    


class provider(db.Model):
    __tablename__="providers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    service_type = db.Column(db.String)

class service(db.Model):
    __tablename__="service_type"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    service_type = db.Column(db.String)