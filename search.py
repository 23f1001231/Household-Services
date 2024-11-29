from model import *
from sqlalchemy import REAL, and_ , or_
from services import *

def search_admin(text):
    search_dict = {
                    "customers" : [],
                    "providers" : [],
                    "service_requests" : []
    }
    def search_by_id():
        # customer
        cust = Customer.query.get(text)
        search_dict["customers"].append(cust)
        # provider
        prov = Provider.query.get(text)
        search_dict["providers"].append(prov)
        # service requests
        service = Service_requests.query.get(text)
        search_dict["service_requests"].append(service)
        return (search_dict)
    def search_by_name_email():
        cust = Customer.query.filter_by(name=text).all()
        if cust != []:
            for i in cust:
                search_dict["customers"].append(i)
        cust = Customer.query.filter_by(email=text).all()
        if cust != []:
            for i in cust:
                search_dict["customers"].append(i)
        prov = Provider.query.filter_by(name=text).all()
        if prov != []:
            for i in prov:
                search_dict["providers"].append(i)
        prov = Provider.query.filter_by(email=text).all()
        if prov != []:
            for i in prov:
                search_dict["providers"].append(i)       
        service_request = Service_requests.query.filter_by(service_name=text).all()
        if service_request != []:
            for i in service_request:
                search_dict["service_requests"].append(i)
        # service_request = Service_requests.query.filter_by(email=text).all()
        # search_dict["service_requests"].append(service_request)


        return (search_dict)


    try:
        text = int(text)
        return search_by_id()
    except:
        return search_by_name_email()

def service_requests_search(search_term,email,user_type):
    search_term = search_term.lower()
    result = []
    if user_type == "customer":
        services = service_requests_list_by_cust(email)
    elif user_type == "provider":
        services = service_requests_list_by_prov_email(email)
    for service in services:
        if str(service.id) == str(search_term):
            result.append(service)
        if service.service_name.lower() == search_term:
            result.append(service)
        if service.customer_name:
            if service.customer_name.lower() == search_term:
                result.append(service)
        if service.provider_name:
            if service.provider_name.lower() == search_term:
                result.append(service)
        if service.customer_email:
            if service.customer_email.lower() == search_term:
                result.append(service)
        if service.provider_email:
            if service.provider_email.lower() == search_term:
                result.append(service)

        if service.request_date == search_term:
            result.append(service)
        if service.completion_date == search_term:
            result.append(service)
    return result





# def service_requests_search(search_term):
#     service_requests_result = Service_requests.query.filter(
#         (Service_requests.service_name.ilike(f'%{search_term}%')) | 
#         (Service_requests.request_date.ilike(f'%{search_term}%')) |
#         (Service_requests.completion_date.ilike(f'%{search_term}%')) |
#         (Service_requests.customer_name == search_term )
#         # (Service_requests.provider_name) == search_term
#     ).all()
#     return service_requests_result

# def service_requests_search(search_term):
#     service_requests = Service_requests.query.filter(
#         Service_requests.customer_name == search_term,
#     ).all()
#     print(Service_requests.customer_name)
#     return service_requests
