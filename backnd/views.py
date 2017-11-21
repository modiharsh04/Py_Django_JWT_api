from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from rest_framework_jwt.views import obtain_jwt_token
import json

from backnd.models import Blog
from backnd.validators import validate_password, validate_email
from backnd.utils import get_token_data, create_login_token

@csrf_exempt
def register(request):
	if request.method != 'POST':
		pass

	post_data = json.loads(request.body.decode('utf-8'))
	username = post_data['username']
	email = post_data['email']
	password = post_data['password']

	try:
	    validate_password(password)
	    validate_email(email)
	except ValidationError as e:
	    return JsonResponse({
	        'status': 'fail',
	        'data': {
	            'message': str(e)
	        }
	    }, status=500)

	if username and password:
		user,created = User.objects.get_or_create(username=username, email=email)
		if created:
			user.set_password(password)
			user.save()
		if user:
			user = authenticate(username=username, password = password)
			return login(request)

	return JsonResponse({'status': 'fail'})

@csrf_exempt
def login(request):
	return obtain_jwt_token(request)

@csrf_exempt
def delete_account(request):
    if request.method != 'DELETE':
        pass
        
    u = User.objects.get(username=username)
    try:
        u.delete()
    except:
        return JsonResponse({
            'status': 'fail',
            'data': {
                'message': 'There was an error while deleting user account'
            }
        }, status=500)

    # need to delete jwt cookie on client side
    return JsonResponse({
        'status': 'success'
    })

@csrf_exempt
def blogs(request):
	blgs = Blog.objects.all()
	lst = []
	for blg in blgs:
		lst.append(blg.get_json())
	data = {'blogs': lst}
	return JsonResponse(data)