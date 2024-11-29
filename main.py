from flask import Flask, render_template as rt, request, redirect, url_for
from model import *
from services import *
from search import *
from graph import *
from sqlalchemy import REAL, and_ , or_
import os
from datetime import datetime

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+ \
os.path.join(current_dir,"Database.sqlite3")

db.init_app(app)
app.app_context().push() # stack in pograming

# graph_service_requests_admin()  

# Login functionality for users and providers
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == "POST":
        EMAIL = request.form["email"]
        PASSWORD = request.form["password"]
        USER_TYPE = request.form["user_type"]

        if USER_TYPE == "customer":
            users = Customer.query.filter_by(email=EMAIL).first()
        if USER_TYPE == "provider":
            users = Provider.query.filter_by(email=EMAIL).first()
            if users.verified != True:
                return "You are not verified by the administration. Please wait for the verification."
            if users.blocked == True:
                return "You have been bocked by the administrator. Please contact the administrator for further information."    
        if USER_TYPE == "admin":
            users = Admin.query.filter_by(email=EMAIL).first()
        if users != None and PASSWORD==users.password: #users can be unbound
            return redirect(url_for("dashboard",user_type=USER_TYPE,email=EMAIL)) 

        else:
            error = 'Wrong Login Credentials !'
            return rt("login.html",error=error)

    return rt("login.html")

# Main dashboard for users (customers,providers,admin)
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    USER_TYPE = request.args.get('user_type')
    if USER_TYPE=="customer":
        EMAIL = request.args.get('email')
        SERVICE_LIST = services_list()
        SERVICE_REQUESTS_LIST = service_requests_list_by_cust(EMAIL)
        return rt("dashboard/customer.html",SERVICE_LIST=SERVICE_LIST,EMAIL=EMAIL,SERVICE_REQUESTS_LIST=SERVICE_REQUESTS_LIST)
    elif USER_TYPE=="provider":
        EMAIL = request.args.get('email')
        prov = prov_details(EMAIL)
        SERVICES_LIST = service_requests_list_by_prov(prov.service_type)
        return rt("dashboard/provider.html",SERVICES_LIST=SERVICES_LIST,SERVICE_DETAILS=service_details,EMAIL=EMAIL)
    elif USER_TYPE=="admin":
        return rt("dashboard/admin.html",services_list=services_list,providers_list=providers_list,customers_list=customers_list,service_requests_list=service_requests_list,service_details=service_details)




# Service form to add,remove,update services
@app.route('/service', methods=['GET','POST'])
def service():
    FROM = request.args.get('from')
    if FROM=="customer_dashboard_new_service":
        SERVICE_NAME = request.args.get('service_name')
        SERVICE_DESC = request.args.get('service_desc')
        SERVICE_BASE_PRICE = request.args.get('service_base_price')
        CUST_EMAIL = request.args.get('cust_email')
        return rt("services/service_add.html",SERVICE_NAME=SERVICE_NAME,SERVICE_DESC=SERVICE_DESC,SERVICE_BASE_PRICE=SERVICE_BASE_PRICE,CUST_EMAIL=CUST_EMAIL)    
    if FROM=="customer_dashboard_close_service":
        SERVICE_ID = request.args.get('service_id')
        CUST_EMAIL = request.args.get('cust_email')
        services_close_by_cust(SERVICE_ID)
        return redirect(url_for("dashboard",user_type="customer",email=CUST_EMAIL))
    if FROM=="customer_dashboard_close_service_page":
        SERVICE_ID = request.args.get('service_id')
        SERVICE_NAME = request.args.get('service_name')
        PROV_NAME = request.args.get('prov_name')
        PROV_EMAIL = request.args.get('prov_email')
        PROV_PH_NO = request.args.get('prov_ph_no')
        print(PROV_PH_NO)
        SERVICE_STATUS = request.args.get('service_status')
        REFERRER = request.referrer
        return rt("services/service_close.html",SERVICE_ID=SERVICE_ID,SERVICE_NAME=SERVICE_NAME,PROV_NAME=PROV_NAME,PROV_EMAIL=PROV_EMAIL,SERVICE_STATUS=SERVICE_STATUS,REFERRER=REFERRER,PROV_PH_NO=PROV_PH_NO)

    if FROM=="provider_dashboard_accept_service":
        PROV_EMAIL = request.args.get('PROV_EMAIL')
        SERVICE_ID = request.args.get('SERVICE_ID')
        service_accept_prov(PROV_EMAIL,SERVICE_ID)
        return redirect(url_for("dashboard",user_type="provider",email=PROV_EMAIL))
    if FROM=="admin_edit_service":
        SERVICE_ID = request.args.get('SERVICE_ID')
        return rt("services/service_edit.html",SERVICE_ID=int(SERVICE_ID),SERVICE_LIST=services_list)
    if FROM=="admin_add_new_service":
        return rt("services/add_new_service.html")
    if FROM=="cust_profile":
        EMAIL = request.args.get('email')
        return rt("profile/customer.html",EMAIL=EMAIL,cust_details=cust_details)
    if FROM=="prov_profile":
        EMAIL = request.args.get('email')
        return rt("profile/provider.html",EMAIL=EMAIL,prov_details=prov_details)

    return "Something went wrong."


# Execute SQL queries
@app.route('/execute', methods=['GET','POST'])
def execute():
    SERVICE_MODE=request.args.get("service_mode")
    if SERVICE_MODE=="add_by_customer":
        SERVICE_NAME=request.args.get("service_name")    
        CUST_EMAIL =request.args.get("cust_email")
        CUST_ID = Customer.query.filter_by(email=CUST_EMAIL).first().id
        REQUEST_DATE = datetime.now().date()
        services_add_by_cust(cust_id=CUST_ID,service_name=SERVICE_NAME,request_date=REQUEST_DATE)
        return redirect(url_for("dashboard",user_type="customer",email=CUST_EMAIL))
    if SERVICE_MODE=="service_edit":
        SERVICE_ID = request.args.get("id")
        SERVICE_NAME = request.args.get("name")
        SERVICE_DESC = request.args.get("desc")
        SERVICE_BASE_PRICE = request.args.get("base_price")
        ADMIN_EMAIL = request.args.get("admin_email")
        service_edit_by_id(SERVICE_ID,SERVICE_NAME,SERVICE_DESC,SERVICE_BASE_PRICE)
        return redirect(url_for("dashboard",user_type="admin",email=ADMIN_EMAIL))
    if SERVICE_MODE=="admin_new_service_add":
        SERVICE_NAME = request.args.get("name")
        SERVICE_DESC = request.args.get("desc")
        SERVICE_BASE_PRICE = request.args.get("base_price")
        ADMIN_EMAIL = request.args.get("admin_email")
        services_new_add_by_admin(SERVICE_NAME,SERVICE_DESC,SERVICE_BASE_PRICE)
        return redirect(url_for("dashboard",user_type="admin",email=ADMIN_EMAIL))
    if SERVICE_MODE=="admin_delete_service":
        SERVICE_ID = request.args.get('SERVICE_ID')
        service_delete_by_id(SERVICE_ID)
        return redirect(url_for("dashboard",user_type="admin"))
    if SERVICE_MODE=="admin_prov_verify":
        PROV_ID = request.args.get('prov_id')
        VERIFIED = request.args.get('verified')
        prov_verification(PROV_ID,VERIFIED)
        return redirect(url_for("dashboard",user_type="admin"))
    if SERVICE_MODE=="admin_delete_prov":
        PROV_ID = request.args.get('prov_id')
        provider_delete_by_id(PROV_ID)
        return redirect(url_for("dashboard",user_type="admin"))        
    if SERVICE_MODE=="admin_delete_service_request":
        SERVICE_REQUEST_ID = request.args.get('service_request_id')
        service_request_delete_by_id(SERVICE_REQUEST_ID)
        return redirect(request.referrer or '/')
        # return redirect(url_for("dashboard",user_type="admin"))        
    if SERVICE_MODE=="admin_prov_blocked":
        PROV_ID = request.args.get('prov_id')
        BLOCK = request.args.get('block')
        prov_block(PROV_ID,BLOCK)
        return redirect(request.referrer or '/')
    if SERVICE_MODE=="admin_remove_cust":
        CUST_ID = request.args.get('cust_id')
        customer_delete_by_id(CUST_ID)
        return redirect(request.referrer or '/')
    if SERVICE_MODE=="cust_ratings_remarks":
        SERVICE_REQUEST_ID = request.args.get('service_id')
        RATING = request.args.get('rating')
        REMARKS = request.args.get('remarks')
        REFERRER = request.args.get('referrer_dashboard')
        service_ratings_remarks(SERVICE_REQUEST_ID,RATING,REMARKS)
        return redirect(REFERRER or '/')
    if SERVICE_MODE=="cust_profile_edit":
        CUST_ID = request.args.get('cust_id')
        NAME = request.args.get('name')
        EMAIL = request.args.get('email')
        ADDRESS = request.args.get('address')
        PIN_CODE = request.args.get('pin_code')
        PH_NO = request.args.get('ph_no')
        PASSWD = request.args.get('passwd')

        cust_edit_details(CUST_ID,NAME,EMAIL,ADDRESS,PIN_CODE,PH_NO,PASSWD)

        return redirect(request.referrer or '/')
    
    if SERVICE_MODE=="prov_profile_edit":
        PROV_ID = request.args.get('prov_id')
        NAME = request.args.get('name')
        EMAIL = request.args.get('email')
        ADDRESS = request.args.get('address')
        PIN_CODE = request.args.get('pin_code')
        PH_NO = request.args.get('ph_no')
        PASSWD = request.args.get('passwd')

        prov_edit_details(PROV_ID,NAME,EMAIL,ADDRESS,PIN_CODE,PH_NO,PASSWD)

        return redirect(request.referrer or '/')
    # if SERVICE_MODE=="admin_delete_service":
    #     SERVICE_REQUEST_ID = request.args.get('service_request_id')
    #     service_request_delete_by_id(SERVICE_REQUEST_ID)
    #     return redirect(request.referrer or '/')


    return "Something went wrong."
        
@app.route("/search",methods=['GET','POST'])
def search():
    FROM = request.args.get('from')
    SEARCH_TEXT = request.args.get('search_text')
    if FROM=="admin":
        RESULT_DICT = search_admin(SEARCH_TEXT)
        return rt("search/admin.html",user_type="admin",RESULT_DICT=RESULT_DICT,service_details=service_details)
    if FROM=="provider":
        PROV_EMAIL = request.args.get('prov_email')
        RESULT_LIST = service_requests_search(SEARCH_TEXT,PROV_EMAIL,"provider")
        return rt("search/provider.html",RESULT_LIST=RESULT_LIST,EMAIL=PROV_EMAIL)
    if FROM=="customer":
        CUST_EMAIL = request.args.get('cust_email')
        RESULT_LIST = service_requests_search(SEARCH_TEXT,CUST_EMAIL,"customer")
        return rt("search/customer.html",user_type="customer",RESULT_LIST=RESULT_LIST,EMAIL=CUST_EMAIL)

@app.route("/summery",methods=['GET','POST'])
def summery():
    FROM = request.args.get('from')
    if FROM=="admin":
        graph_ratings_admin()
        graph_service_requests_admin()
        return rt("graph/admin.html")
    if FROM=="customer":
        CUST_EMAIL = request.args.get('cust_email')
        graph_service_requests_users(CUST_EMAIL,"customer")
        return rt("graph/customer.html",EMAIL=CUST_EMAIL)
    if FROM=="provider":
        PROV_EMAIL = request.args.get('prov_email')
        graph_ratings_provider(PROV_EMAIL)
        graph_service_requests_users(PROV_EMAIL,"provider")
        return rt("graph/provider.html",EMAIL=PROV_EMAIL)


@app.route("/register_cust",methods=['GET','POST'])
def register_cust():
    if request.method == "POST":

        NAME = request.form["name"]
        EMAIL = request.form["email"]
        PASSWORD = request.form["password"]
        ADDRESS = request.form["address"]
        PIN_CODE = request.form["pin_code"]
        PH_NO = request.form["ph_no"]

        cust_add(NAME,EMAIL,PASSWORD,ADDRESS,PIN_CODE,PH_NO)

        return rt("login.html")

    return rt("registration/customer.html")

@app.route("/register_prov",methods=['GET','POST'])
def register_prov():
    if request.method == "POST":

        NAME = request.form["name"]
        EMAIL = request.form["email"]
        PASSWORD = request.form["password"]
        ADDRESS = request.form["address"]
        PIN_CODE = request.form["pin_code"]
        PH_NO = request.form["ph_no"]
        SERVICE_TYPE = request.form["service_type"]
        EXP = request.form["exp"]

        prov_add(NAME,EMAIL,PASSWORD,ADDRESS,PIN_CODE,PH_NO,SERVICE_TYPE,EXP)

        return rt("login.html")

    return rt("registration/provider.html")

@app.route("/form_tester",methods=['GET','POST'])
def form_tester():
    return "fine"

if __name__ == "__main__":
    db.create_all()
   
    app.debug = True
    app.run(host='0.0.0.0')


