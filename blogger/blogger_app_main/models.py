from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class Blog(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	total_followed = models.IntegerField()
	total_posts = models.IntegerField()

class Post(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	header = models.CharField(max_length=100)
	text = models.CharField(max_length=5000)
	date_created = models.DateTimeField(default=now)
	total_read = models.IntegerField()

class Follow(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


class Read(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)


