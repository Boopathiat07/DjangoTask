from django.http import JsonResponse
from .common import decode_jwt_token, get_user, handling_badrequest, get_session

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_path = ['/login','/create_user','/hello','/google_view','/auth_login','/auth/google/callback','/employees']

        if request.path in url_path or request.path.startswith("/api/v2"):
            return self.get_response(request)

        authorization_header = request.headers.get('Authorization')
        if not authorization_header or not authorization_header.startswith('Bearer '):
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        token = authorization_header.split(' ')[1]
        payload = decode_jwt_token(token)

        jti = payload['jti']
        user_id = payload['user_id']
        try:
            user = get_user(request=request,user_id=user_id)
        except Exception as e:
            return handling_badrequest(str(e))
        jti_data = get_session(request=request,jti=jti)
        if not user:
            return handling_badrequest("Invalid Token user")
        
        if not jti_data:
            return handling_badrequest("No Session found")
        
        if jti_data.islogin==False:
            return handling_badrequest("Session Expired")
        
        
        request.META['jti'] = str(jti)
        request.META['user_id'] = str(user_id)
        
        return self.get_response(request)
       