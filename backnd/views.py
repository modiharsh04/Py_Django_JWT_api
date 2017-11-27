from backnd.authView import *

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

@csrf_exempt
def newPost(request):
	if request.method != 'POST':
		return JsonResponse({
			'status' : 'fail',
			'data' : 'Wrong Method Call'
			})

	post_data = json.loads(request.body.decode('utf-8'))
	try:
		author = post_data.get('author')
		author = User.objects.get(username = author.get('username'))
		b = Blog()
		b.subject = post_data.get('subject')
		b.content = post_data.get('content')
		b.author = author
		b.save();
		return JsonResponse({
			'status' : 'success',
			'data' : b.get_json()
			}, status=200)
	except Exception as err:
		return JsonResponse({
			'status' : 'fail',
			'data' : {'err':'Could not add post, try later',
					  'message':err}
			}, status=500)


	return JsonResponse({
		'status' : 'fail',
		'data' : 'Could not add post, try later'
		}, status=500)