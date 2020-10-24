from django.http import HttpResponse,JsonResponse
from django.views import View

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
#from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .models import Blog,Post,Read,Follow
from django.contrib.auth.models import User 

from django.utils.decorators import method_decorator
from .decorators import tokin_required

class AllArticlesView(View):

	def get(self, request, *args, **kwargs):
		data = {"Im here":"That's true"}
		return JsonResponse(data)

class SubsribedArticlesView(View):
	#permission_classes = [IsAuthenticated]
	#authentication_classes = [TokenAuthentication]
	@method_decorator(tokin_required)
	def get(self, request, *args, **kwargs):
		print("User id from request ",request.user.id)
		data = {"Youre":"Authorized"}
		return JsonResponse(data)

class AuthView(ObtainAuthToken):

	def post(self, request):
		serializer = self.serializer_class(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		data={
		'token':token,
		'user_id': user.pk,
		'email': user.email
		}
		return JsonResponse(data)