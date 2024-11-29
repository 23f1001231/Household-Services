from flask_sqlalchemy import SQLAlchemy                                                                                   

db = SQLAlchemy()                                                                                                         

class Customer(db.Model):                                                                                                    
    __tablename__="customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    ph_no = db.Column(db.Integer)
    address = db.Column(db.String)
    pin_code = db.Column(db.Integer)
    
    services = db.relationship('Service_requests', backref='customer', lazy=True)



class Provider(db.Model):
    __tablename__="providers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    verified = db.Column(db.Boolean, default=False)
    blocked = db.Column(db.Boolean, default=False)
    service_type = db.Column(db.String)
    experience = db.Column(db.Integer)
    ph_no = db.Column(db.Integer)
    address = db.Column(db.String)
    pin_code = db.Column(db.Integer)
    
    services = db.relationship('Service_requests', backref='provider', lazy=True)

class Services(db.Model):
    __tablename__="services"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)
    base_price = db.Column(db.Integer, nullable=False)
    formal_name = db.Column(db.String, nullable=False)
    
    

class Service_requests(db.Model):
    __tablename__="service_requests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    service_name = db.Column(db.String, nullable=False)
    prov_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=True)
    request_date = db.Column(db.Date, nullable=False)
    completion_date = db.Column(db.Date, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    service_status = db.Column(db.String)
    remarks = db.Column(db.String)

# Property to get the customer's name
    @property
    def customer_name(self):
        customer = Customer.query.get(self.cust_id)
        return customer.name if customer else None
# Property to get the customer's email
    @property
    def customer_email(self):
        customer = Customer.query.get(self.cust_id)
        return customer.email if customer else None
# Property to get the provider's name
    @property
    def provider_name(self):
        provider = Provider.query.get(self.prov_id)
        return provider.name if provider else None   
 # Property to get the provider's email
    @property
    def provider_email(self):
        provider = Provider.query.get(self.prov_id)
        return provider.email if provider else None 
 # Property to get the provider's phone number
    @property
    def provider_ph_no(self):
        provider = Provider.query.get(self.prov_id)
        return provider.ph_no if provider else None 
class Admin(db.Model):                                                                                                    
    __tablename__="admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
