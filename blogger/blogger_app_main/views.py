from django.http import HttpResponse,JsonResponse
from django.views import View
from django.http import QueryDict

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
#from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .models import Blog,Post,Read,Follow
from django.contrib.auth.models import User

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

class AllArticlesView(View):

	def get(self, request, *args, **kwargs):
		news = Post.objects.order_by('-date_created').all()[0:5]
		blogs = Blog.objects.order_by('-total_followed').all()
		data = {
		'news':[{'id':article.id, 'header':article.header,'text':article.text,'date':article.date_created, 'totalR':article.total_read} for article in news],
		'blogs':[{'id':blog.id, 'name':blog.name,'totalF':blog.total_followed,'totalP':blog.total_posts} for blog in blogs],
		}
		return JsonResponse(data)


class SubsribedArticlesView(APIView):
	permission_classes = [IsAuthenticated]
	#authentication_classes = [TokenAuthentication]

	def get(self, request, *args, **kwargs):
		print("User id from request ",request.user.id)
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


class FollowView(APIView):
	permission_classes = [IsAuthenticated]
	
	@method_decorator(ensure_csrf_cookie)
	def get(self, request):
		follows = Follow.objects.filter(user=request.user)
		return Response({
			'follows':[follow.blog.id for follow in follows]
			})

	def post(self, request):
		blog = Blog.objects.get(pk=request.POST.get('blog_id'))
		new_follow = Follow(user=request.user,blog=blog)
		new_follow.save()
		return Response({
			'followed':{
			'user':new_follow.user.username,
			'blog':new_follow.blog.name
			}
			})

	def delete(self, request):
		delete_p = QueryDict(request.body)
		blog = Blog.objects.get(pk=delete_p.get('blog_id'))
		del_obj = Follow.objects.get(user=request.user,blog=blog)
		del_obj.delete()
		return Response({
			'unfollowed':{
			'user':del_obj.user.username,
			'blog':del_obj.blog.name
			}
			})


class ReadView(APIView):
	permission_classes = [IsAuthenticated]
	
	@method_decorator(ensure_csrf_cookie)
	def get(self, request):
		reads = Read.objects.filter(user=request.user)
		return Response({
			'reads':[read.post.id for read in reads]
			})

	def post(self, request):
		post = Post.objects.get(pk=request.POST.get('post_id'))
		new_read = Read(user=request.user,blog=post.blog,post=post)
		new_read.save()
		return Response({
			'reading':{
			'user':new_read.user.username,
			'blog':new_read.blog.name,
			'post':new_read.post.header,
			}
			})

	def delete(self, request):
		delete_p = QueryDict(request.body)
		post = Post.objects.get(pk=delete_p.get('post_id'))
		del_obj = Read.objects.get(user=request.user,blog=post.blog, post=post)
		del_obj.delete()
		return Response({
			'unread':{
			'user':del_obj.user.username,
			'blog':del_obj.blog.name,
			'post':del_obj.post.header,
			}
			})










