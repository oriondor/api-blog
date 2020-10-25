from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class Blog(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=20, default='My Blog')
	total_followed = models.IntegerField(default=0)
	total_posts = models.IntegerField(default=0)

class Post(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	header = models.CharField(max_length=100)
	text = models.CharField(max_length=5000)
	date_created = models.DateTimeField(default=now)
	total_read = models.IntegerField(default=0)

class Follow(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


class Read(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
