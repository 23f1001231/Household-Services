from flask_sqlalchemy import SQLAlchemy                                                                                   

db = SQLAlchemy()                                                                                                         

class Customer(db.Model):                                                                                                    
    __tablename__="customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    
    services = db.relationship('Services', backref='customer', lazy=True)


class Provider(db.Model):
    __tablename__="providers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    status = db.Column(db.String)
    service_type = db.Column(db.String)

class Services(db.Model):
    __tablename__="service_type"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    service_type = db.Column(db.String)

    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

