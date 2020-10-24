from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from functools import wraps

def tokin_required(function):
	@wraps(function)
	def wrap(request, *args, **kwargs):
		print(request.method,request.headers)
		username = Token.objects.get(key=request.headers['Tokin'].split(' ')[1]).user
		user = User.objects.get(username=username)
		if user:
			request.user=user
			return function(request, *args, **kwargs)
		else:
			raise PermissionDenied
	#wrap.__doc__ = function.__doc__
	#wrap.__name__ = function.__name__
	return wrap