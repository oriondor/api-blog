from django.http import HttpResponse,JsonResponse
from django.views import View
from django.http import Http404
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

	def head(self, request, *args, **kwargs):
		news = Post.objects.latest('date_created')
		response = HttpResponse()
		response['Last-Modified'] = news.date_created.strftime('%a, %d %b %Y %H:%M:%S GMT')
		news = Post.objects.order_by('-date_created').all()
		blogs = Blog.objects.order_by('-total_followed').all()
		ag_summ = 0
		for art in news:
			ag_summ += art.total_read
		for blog in blogs:
			ag_summ += blog.total_followed
		response['Content-Length'] = ag_summ
		return response


	@method_decorator(ensure_csrf_cookie)
	def get(self, request, *args, **kwargs):
		if 'article' in self.kwargs:
			article = Post.objects.get(pk=self.kwargs['article'])
			if not article:
				raise Http404
			return JsonResponse({
				'article':{
					'id':article.id, 
					'header':article.header,
					'text':article.text,
					'date':article.date_created, 
					'totalR':article.total_read
				}
				})
		news = Post.objects.order_by('-date_created').all()[0:5]
		blogs = Blog.objects.order_by('-total_followed').all()
		data = {
		'news':[{
			'id':article.id, 'header':article.header,'text':article.text,'date':article.date_created, 'totalR':article.total_read
				} for article in news],
		'blogs':[{
			'id':blog.id, 'name':blog.name,'totalF':blog.total_followed,'totalP':blog.total_posts
				} for blog in blogs],
		}
		return JsonResponse(data)



class SubsribedArticlesView(APIView):
	permission_classes = [IsAuthenticated]
	#authentication_classes = [TokenAuthentication]

	def head(self, request, *args, **kwargs):
		follows = Follow.objects.filter(user=request.user)
		followed_blogs = []
		for follow in follows:
			followed_blogs.append(Blog.objects.get(pk=follow.blog.id))
		news = Post.objects.filter(blog__in=followed_blogs)
		blogs = Blog.objects.order_by('-total_followed').all()
		response = HttpResponse()
		response['Last-Modified'] = news.latest('date_created').date_created.strftime('%a, %d %b %Y %H:%M:%S GMT')
		ag_summ = 0
		for art in news:
			ag_summ += art.total_read
		for blog in blogs:
			ag_summ += blog.total_followed
		response['Content-Length'] = ag_summ
		return response


	@method_decorator(ensure_csrf_cookie)
	def get(self, request, *args, **kwargs):
		follows = Follow.objects.filter(user=request.user)
		followed_blogs = []
		for follow in follows:
			followed_blogs.append(Blog.objects.get(pk=follow.blog.id))
		news = Post.objects.filter(blog__in=followed_blogs).order_by('-date_created').all()
		blogs = Blog.objects.order_by('-total_followed').all()
		data = {
		'news':[{
			'id':article.id, 'header':article.header,'text':article.text,'date':article.date_created, 'totalR':article.total_read
				} for article in news],
		'blogs':[{
			'id':blog.id, 'name':blog.name,'totalF':blog.total_followed,'totalP':blog.total_posts
				} for blog in blogs],
		}
		return Response(data)

	def post(self, request):
		header = request.POST.get('header')
		text = request.POST.get('text')
		if header and text:
			new_post = Post(blog=Blog.objects.get(user=request.user),header=header,text=text)
			new_post.save()
			return Response({
				'posted':{
				'header':new_post.header,
				'blog':new_post.blog.name,
				}
				})
		return Response({
			'error':"Post couldn't be created now!\nSet appropriate arguments first;"
			})



class AuthView(ObtainAuthToken):

	@method_decorator(ensure_csrf_cookie)
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
		try:
			Follow.objects.get(user=request.user,blog=post.blog)
		except:
			new_follow = Follow(user=request.user,blog=post.blog)
			new_follow.save()
		finally:
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










