import bcrypt
from django.http.response import JsonResponse as Response
import jwt
from django.conf import settings
from operation.models import User, Session
from datetime import datetime, timedelta
from .serializers import SessionForms
import uuid
from django.core.cache import cache

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    return hashed_password

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def response(data):
    return Response({"message":"OK", "body":data}, status =200)

def handling_server(data):
    return Response({"error":data}, status=500)

def handling_badrequest(data):
    return Response({"error":data},status=400)

def return_key(request, *args, **kwargs):
    jti  = request.META.get('jti')
    return request.path+'/'+jti

uniqueId = str(uuid.uuid4())
logintime = datetime.utcnow()

def generate_jwt_token(id):
    payload = {
        'jti': uniqueId,
        'Uid': id,
        'exp': logintime + timedelta(days=1), 
        'iat': logintime  
    }

    session_data = {
        'jti' : uniqueId,
        'login_time' : logintime,
        'islogin' : True,
        'email' : id,
        'logout_time': logintime
    }
         
    session_form = SessionForms(data=session_data)

    if session_form.is_valid():
        session_form.save()
    else:
        return handling_badrequest("No session Found")

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['Uid']
        jti = payload['jti']

        print("jti :",jti)
        
        data = { 
            'jti':jti,
            'user_id':user_id
        }

        return data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
def get_user(request, user_id):
    user_cache_key = user_id
    user = cache.get(user_cache_key)
    if not user:
        user = User.objects.get(email=user_id)
        cache.set(user_cache_key, user)
    return user

def get_session(request, jti):
    session_cache_key = jti

    session = cache.get(session_cache_key)
    
    if not session:
        session = Session.objects.get(jti=jti)
        cache.set(session_cache_key, session)
    return session

        


