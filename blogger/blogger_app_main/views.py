from django.http import HttpResponse,JsonResponse
from django.views import View


class ShowView(View):

	def get(self, request, *args, **kwargs):
		data = {"Im here":"That's true"}
		return JsonResponse(data)
