from django.http import HttpResponse,JsonResponse
from django.views import View

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
#from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

class AllArticlesView(View):

	def get(self, request, *args, **kwargs):
		data = {"Im here":"That's true"}
		return JsonResponse(data)

class SubsribedArticlesView(APIView):
	permission_classes = [IsAuthenticated]
	#authentication_classes = [TokenAuthentication]

	def get(self, request, *args, **kwargs):
		data = {"Youre":"Authorized"}
		return Response(data)

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