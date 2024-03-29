from django.http.response import JsonResponse as Response

def response(data):
    return Response({"message":"OK", "body":data}, status =200)

def handling_server(data):
    return Response({"error":data}, status=500)

def handling_badrequest(data):
    return Response({"error":data},status=400)