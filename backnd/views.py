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
from backnd.utils import get_token_data,get_user

@csrf_exempt
def register(request):
	if request.method != 'POST':
		pass

	post_data = json.loads(request.body.decode('utf-8'))
	username = post_data.get('username')
	email = post_data.get('email')
	password = post_data['password']
	first_name = post_data.get('first_name','Anonymous')
	last_name = post_data.get('last_name','Anonnymous')

	try:
	    validate_password(password)
	    validate_email(email)
	except ValidationError as e:
	    return JsonResponse({
	        'status': 'fail',
	        'data': {
	            'status': str(e)
	        }
	    }, status=500)

	if username and password:
		user,created = User.objects.get_or_create(username=username, email=email)
		if created:
			try:
				user.set_password(password)
				user.save()
			except:
				return JsonResponse({'status': 'fail'})

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
        
    user = get_token_data(request)
    u = User.objects.get(username=user.get('username'))
    try:
        u.delete()
    except:
        return JsonResponse({
            'status': 'fail',
            'data': {
                'message': 'There was an error while deleting user account'
            }
        }, status=500)

    return JsonResponse({
        'status': 'success'
    })

@csrf_exempt
def blogs(request):
	if request.method != 'GET':
		return JsonResponse({
			'status' : 'fail - Wrong Method call'
			})

	blgs = Blog.objects.order_by('last_modified')[:10]
	lst = []
	for blg in blgs:
		lst.append(blg.get_json())
	data = {'blogs': lst}
	return JsonResponse(data)

@csrf_exempt
def user(request):
	if request.method != 'GET':
		return JsonResponse({
			'status' : 'fail',
			'data' : 'Wrong Method Call'
			})

	user = get_token_data(request)
	u = User.objects.get(username = user.get('username'))
	if u:
		return JsonResponse({
			'status' : 'success',
			'data' : get_user(u)
			})
	else:
		return JsonResponse({
			'status' : 'fail',
			'data' : 'Could not find user'
			})

@csrf_exempt
def author(request,username):
	if request.method != 'GET':
		return JsonResponse({
			'status' : 'fail',
			'data' : 'Wrong Method Call'
			})

	u = User.objects.get(username = username)
	if u:
		return JsonResponse({
			'status' : 'success',
			'data' : get_user(u)
			})
	else:
		return JsonResponse({
			'status' : 'fail',
			'data' : 'Could not find user'
			})