from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from .models import Blog,Post,Read,Follow
from django.db.models import F

from django.core.mail import send_mail


@receiver(post_save, sender=Follow)
def increment_follows_counter(sender, instance, created, **kwargs):
	if created:
		blog = Blog.objects.get(pk=instance.blog.id)
		blog.total_followed = F('total_followed')+1
		blog.save()


@receiver(post_delete, sender=Follow)
def decrement_follows_counter(sender, instance, **kwargs):
	blog = Blog.objects.get(pk=instance.blog.id)
	blog.total_followed = F('total_followed')-1
	blog.save()
	reads = Read.objects.filter(user=blog.user,blog=blog)
	for read in reads:
		post = Post.objects.get(blog=read.blog)
		post.total_read = F('total_read')-1
		post.save()
	reads.delete()


@receiver(post_save, sender=Read)
def increment_read_counter(sender, instance, created, **kwargs):
	if created:
		post = Post.objects.get(pk=instance.post.id)
		post.total_read = F('total_read')+1
		post.save()


@receiver(post_delete, sender=Read)
def decrement_read_counter(sender, instance, **kwargs):
	post = Post.objects.get(pk=instance.post.id)
	post.total_read = F('total_read')-1
	post.save()


@receiver(post_save, sender=Post)
def new_post_signal(sender, instance, created, **kwargs):
	if created:
		blog = Blog.objects.get(pk=instance.blog.id)
		followers = Follow.objects.filter(blog=blog).all()
		emails = [User.objects.get(pk=follower.user.id).email for follower in followers]
		subject = "Blogger - New post from the person you followed"
		link = f"https://blogger-frontend-node.herokuapp.com/?article={instance.id}"
		message = f"There is a new post in {blog.name}. You can read it by following link {link}."
		send_mail(subject,message,'admin@blogger.com',emails)




