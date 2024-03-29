from django.http import HttpResponse
from operation.serializers import UserSerializer, EmployeeSerializer
from operation.models import User, Employee
from .common import response, handling_server, handling_badrequest, generate_jwt_token, verify_password, hash_password, get_session,get_user, return_key
import json
from datetime import datetime
from django.core.mail import send_mail
from django.views.decorators.cache import cache_page
from django.views import View
from django.utils.decorators import method_decorator
import requests
import traceback

import os 
from dotenv import load_dotenv
load_dotenv()

# @method_decorator(cache_page(60*2), name='dispatch') #It will cache all methods inside the class
class UserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            data['password'] = hash_password(data['password'])
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return response("User Added SuccessFully")
                
            return handling_badrequest(serializer.errors)
        except Exception as e:
            return handling_server(str(e))

    # @cache_page(60*2) #error occurs due to @cache_page syntax.by annotating cache page it does not consider as get method function. it defines as normal function.
    def get(self, request):
        try:
            user_id  = request.META.get('user_id')
            if user_id is None:
                return handling_server("No User id Found")

            user = get_user(request=request,user_id=user_id)
        
            user_data = {
                "id":user.id,
                "name" : user.name,
                "email":user.email,
                "mobile_no":user.mobile_no
            }
            
            return response(user_data)
            
        except Exception as e:
            return handling_server(str(e))

    def put(self, request):
        try:
            data = json.loads(request.body)

            user_id  = request.META.get('user_id')
            user = get_user(request=request,user_id=user_id)
            
            user.name = data['name']

            user.save()
            return response("Updated SuccesFully")

        except Exception as e:
            return handling_server(str(e))

    def delete(self, request):
        try:
            data = json.loads(request.body)

            user = User.objects.get(email=data['email'])

            user.delete()

            return response("User Deleted SuccessFully")
        except Exception as e:
            return handling_server(str(e))


class EmployeeView(View):
    def post(self, request):
        try:    
            data = json.loads(request.body)

            emp_data = EmployeeSerializer(data=data)
           
            if emp_data.is_valid():
                emp_data.save()
                return response("User Added SuccessFully")
                
            return handling_badrequest("invalid")

            # name = data['name']
            # email = data['email']
            # mobile_no = data['mobile_no']
            # employee = {
            #     "name" : name,
            #     "email" : email,
            #     "mobile_no" : mobile_no
            # }

        
        except Exception as e:
            traceback.print_exception(e)
            return handling_server(str(e))

    def get(self, request):
        try:
            employes_data = Employee.objects.filter().all()
            
            employees = []
            for i in employes_data:
                emp = {
                    "name" : i.name,
                    "email" : i.email,
                    "mobile_no": i.mobile_no
                }
                employees.append(emp)

            return response(employees)

        
        except Exception as e:
            return handling_server(str(e))

    def put(self, request):
        try:
            data = json.loads(request.body)

            email = data['email']
            name = data['name']
            mobile_no = data['mobile_no']

            employee = Employee.objects.filter(email=email).first()

            employee.name = name
            employee.mobile_no = mobile_no

            employee.save()
            
            return response("User updated SuccessFully")

        except Exception as e:
            return handling_server(str(e))

    def delete(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            employee = Employee.objects.filter(email=email).all()

            employee.delete()
            return response("User Deleted SuccessFully")

        except Exception as e:
            return handling_server(str(e))

    
def login(request):
    try:
        data = json.loads(request.body)
        
        email = data['email']
        password = data['password']
         
        user = User.objects.get(email=email)
          
        if verify_password(password, user.password):
            id = user.email
            token = generate_jwt_token(id)
            return response(token)

        return handling_badrequest("Credentials Mismatch")
                
    except Exception as e:
        return handling_server(str(e))
    

def logout(request):
    jti  = request.META.get('jti')
    
    session_data = get_session(request=request, jti=jti)
    
    session_data.islogin = False
     
    logouttime = datetime.now()

    session_data.logout_time = logouttime

    session_data.save()

    return response("Loggedout Successfully !")

class GoogleView(View):
    def post(self, request):
        # token = {'id_token': request.data.get('id_token')}
        # print(token)
        import time
        data = json.loads(request.body)
         
        token = data['id_token'] 

        url = f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'

        try:
            response_data = requests.get(url)
            res = response_data.json()
            return response(res)

        except Exception as e:
            return handling_badrequest(str(e))
        
        

@cache_page(60*1, key_prefix=return_key)
def home(request):
    print("hey !!")
    return HttpResponse("Hello World !!!")

def send_hello():
    time = datetime.datetime.now()
    subject = 'Welcome to Django'
    message = 'Thank you !!!....................................'
    from_email = 'boopathig158@gmail.com'
    recipient_list = ['boopathiboopathi7647@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
    print('Mail Send :[{}]'.format(time))

def create_user(request):
    try:
        data = json.loads(request.body)
        data['password'] = hash_password(data['password'])
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return response("User Added SuccessFully")
              
        return handling_badrequest(serializer.errors)
    except Exception as e:
        return handling_server(str(e))
    


@cache_page(60*2, key_prefix=return_key)
def fetch_user(request):
    try:
        user_id  = request.META.get('user_id')
        user = get_user(request=request,user_id=user_id)
    
        user_data = {
            "id":user.id,
            "name" : user.name,
            "email":user.email,
            "mobile_no":user.mobile_no
        }
        
        return response(user_data)
        
    except Exception as e:
        return handling_server(str(e))
        
def update_user(request):
    try:
        data = json.loads(request.body)

        user_id  = request.META.get('user_id')
        user = get_user(request=request,user_id=user_id)
        
        user.name = data['name']

        user.save()
        return response("Updated SuccesFully")

    except Exception as e:
        return handling_server(str(e))


def delete_user(request):
    try:
        data = json.loads(request.body)

        user = User.objects.get(email=data['email'])

        user.delete()

        return response("User Deleted SuccessFully")
    except Exception as e:
        return handling_server(str(e))
    

from django.shortcuts import redirect
from django.http import HttpResponse
import requests

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

def google_auth_redirect(request):
    google_auth_url = (
        'https://accounts.google.com/o/oauth2/auth?response_type=code'
        '&client_id={}&redirect_uri={}&scope=email profile'
        '&state=random_state_string'.format(
            GOOGLE_CLIENT_ID,
            'http://localhost:8000/auth/google/callback'  
        )
    )
    return redirect(google_auth_url)

def google_auth_callback(request):
    code = request.GET.get('code')
    token_endpoint = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': 'http://localhost:8000/auth/google/callback',  
        'grant_type': 'authorization_code',
    }
    res = requests.post(token_endpoint, data=token_data)
    if res.status_code == 200:
        token_response = res.json()
        access_token = token_response['access_token']
        refresh_token = token_response.get('refresh_token')
        id_token = token_response['id_token'] 
        
        tokens = {
            "accessToken":access_token,
            "refresgToken" :refresh_token,
            "idToken":id_token
        }
        return response(tokens)
    else:
        return handling_server("Authentication failed!")
