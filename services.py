from model import *
from datetime import datetime

def services_list():
    services = db.session.query(Services).all()
    return services

def service_requests_list():
    service_requests = db.session.query(Service_requests).all()
    return service_requests

def providers_list():
    providers = db.session.query(Provider).all()
    return providers

def customers_list():
    customers = db.session.query(Customer).all()
    return customers

def service_requests_list_by_cust(cust_email):
    cust_id = Customer.query.filter_by(email=cust_email).first().id
    service = Service_requests.query.filter_by(cust_id=cust_id).all()
    return service

def service_requests_list_by_prov_email(prov_email):
    prov_id = Provider.query.filter_by(email=prov_email).first().id
    service = Service_requests.query.filter_by(prov_id=prov_id).all()
    return service   

def service_requests_list_by_prov(service_type):
    service = Service_requests.query.filter_by(service_name=service_type).all()
    return service



def services_add_by_cust(cust_id,service_name,request_date):
    new_service=Service_requests(
        cust_id = cust_id,
        service_name = service_name,
        request_date = request_date,
        service_status = "Requested"
        )
    db.session.add(new_service)
    db.session.commit()

def services_close_by_cust(service_id):
    service = Service_requests.query.get(service_id)
    service.service_status = "Completed"
    service.completion_date= datetime.now().date()
    db.session.commit()

def prov_details(prov_email):
    details = Provider.query.filter_by(email=prov_email).first()
    return details

def cust_details(cust_email):
    details = Customer.query.filter_by(email=cust_email).first()
    return details

def service_details(service_id):
    service_details = Service_requests.query.filter_by(id=service_id).first()
    cust_details = Customer.query.filter_by(id=service_details.cust_id).first()
    prov_details = Provider.query.filter_by(id=service_details.prov_id).first()

    service_details_dict = {
                            'service' :  service_details,
                            'customer' : cust_details,
                            'prov_details' : prov_details
    }
    return service_details_dict

def service_accept_prov(prov_email,service_id):
    prov_id = prov_details(prov_email).id
    service = Service_requests.query.get(service_id)
    service.prov_id = prov_id
    service.service_status = "Assigned"
    db.session.commit()

def service_edit_by_id(service_id,service_name,service_desc,service_base_price):
    service = Services.query.get(service_id)
    service.formal_name = service_name
    service.desc = service_desc
    service.base_price = service_base_price
    db.session.commit()

def service_delete_by_id(service_id):
    service = Services.query.get(service_id)  
    if service:
        db.session.delete(service)  
        db.session.commit()  

def service_delete_by_id(service_id):
    service = Services.query.get(service_id)  
    if service:
        db.session.delete(service)  
        db.session.commit()

def service_delete_by_cust_id(cust_id):
    services = Service_requests.query.filter_by(cust_id=cust_id).all()
    for service in services:
        if service:
            db.session.delete(service)  
            db.session.commit()

def services_new_add_by_admin(service_name,service_desc,service_base_price):
    new_service=Services(
        name = service_name,
        formal_name = service_name,
        desc = service_desc,
        base_price = service_base_price,
        )
    db.session.add(new_service)
    db.session.commit()

def prov_verification(prov_id,verified):
    prov = Provider.query.get(prov_id)  
    prov.verified = bool(int(verified))
    db.session.commit()

def provider_delete_by_id(prov_id):
    prov = Provider.query.get(prov_id)  
    if prov:
        db.session.delete(prov)  
        db.session.commit()  

def service_request_delete_by_id(service_request_id):
    service_request = Service_requests.query.get(int(service_request_id))  
    if service_request:
        db.session.delete(service_request)  
        db.session.commit()  

def prov_block(prov_id,blocked):
    prov = Provider.query.get(prov_id)  
    prov.blocked = bool(int(blocked))
    db.session.commit()

def customer_delete_by_id(cust_id):
    service_delete_by_cust_id(cust_id)
    cust = Customer.query.get(cust_id)  
    if cust:
        db.session.delete(cust)  
        db.session.commit()  

def service_ratings_remarks(service_request_id,rating,remarks):
    request = Service_requests.query.get(service_request_id)
    request.rating = rating
    request.remarks = remarks
    db.session.commit()


def cust_add(name,email,password,address,pin_code,ph_no):
    new_cust=Customer(
        name = name,
        email = email,
        password = password,
        ph_no = ph_no,
        address = address,
        pin_code = pin_code
        )
    db.session.add(new_cust)
    db.session.commit()

def prov_add(name,email,password,address,pin_code,ph_no,service_type,exp):
    new_prov=Provider(
        name = name,
        email = email,
        password = password,
        ph_no = ph_no,
        address = address,
        pin_code = pin_code,
        experience = exp,
        service_type = service_type,
        blocked = False,
        verified = False
        )
    db.session.add(new_prov)
    db.session.commit()

def cust_edit_details(cust_id,name,email,address,pin_code,ph_no,password):
    cust = Customer.query.get(cust_id) 
    cust.name = name
    cust.email = email
    cust.address = address
    cust.pin_code = pin_code
    cust.ph_no = ph_no
    cust.password = password
    db.session.commit()

def prov_edit_details(prov_id,name,email,address,pin_code,ph_no,password):
    prov = Provider.query.get(prov_id) 
    prov.name = name
    prov.email = email
    prov.address = address
    prov.pin_code = pin_code
    prov.ph_no = ph_no
    prov.password = password
    db.session.commit()
