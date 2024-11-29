from model import *
from services import *

import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

import os

def graph_ratings_provider(prov_email):
    ratings = {
            "5" : 0,
            "4" : 0,
            "3" : 0,
            "2" : 0,
            "1" : 0,
    }
    service_requests_list = service_requests_list_by_prov_email(prov_email)
    for service in service_requests_list:
        if service.rating:
            ratings[str(service.rating)] += 1
    y = [ratings[x] for x in ratings]
    labels = ["1","2","3","4","5"]
    plt.pie(y, labels=labels)
    plt.legend(title = "Ratings")
    plt.title('Overall Ratings')
    plt.savefig("static/plots/ratings_provider.png") 
    plt.close()


def graph_ratings_admin():
    ratings = {
            "5" : 0,
            "4" : 0,
            "3" : 0,
            "2" : 0,
            "1" : 0,
    }
    service_requests = service_requests_list()
    for service in service_requests:
        if service.rating:
            ratings[str(service.rating)] += 1
    y = [ratings[x] for x in ratings]
    labels = [x for x in ratings]
    plt.pie(y, labels=labels)
    plt.legend()
    plt.legend(title = "Ratings")
    plt.title("Overall Ratings")
    plt.savefig("static/plots/ratings_admin.png") 
    plt.close()

def graph_service_requests_users(email,user_type):
    service_status = {
            "Requested" : 0,
            "Assigned" : 0,
            "Completed" : 0
    }
    
    if user_type == "provider":
        service_requests_list = service_requests_list_by_prov_email(email)
    if user_type == "customer":
        service_requests_list = service_requests_list_by_cust(email)

    for service in service_requests_list:
        if service.service_status:
            service_status[service.service_status] += 1
    y = [service_status[x] for x in service_status]
    x = [x for x in service_status]
    plt.bar(x,y)
    plt.title("Service Status")
    plt.savefig(f"static/plots/service_request_status_{user_type}.png")     
    plt.close()

def graph_service_requests_admin():
    service_status = {
            "Requested" : 0,
            "Assigned" : 0,
            "Completed" : 0
    }
    
    service_requests = service_requests_list()
    for service_request in service_requests:
        if service_request.service_status:
            service_status[service_request.service_status] += 1
    y = [service_status[x] for x in service_status]
    x = [x for x in service_status]
    plt.bar(x,y)
    plt.legend(title = "Service Status")
    plt.title("Service Status")
    plt.savefig("static/plots/service_request_status_admin.png")     
    plt.close()

def graph_service_requests_admin():
    service_status = {
            "Requested" : 0,
            "Assigned" : 0,
            "Completed" : 0
    }
    

    service_requests = service_requests_list()

    for service in service_requests:
        if service.service_status:
            service_status[service.service_status] += 1
    y = [service_status[x] for x in service_status]
    x = [x for x in service_status]
    plt.bar(x,y)
    plt.title("Service Status")
    plt.savefig("static/plots/service_request_status_admin.png")     
    plt.close()