# -*- coding: utf-8 -*-
import datetime, logging
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete

def add_post_signal(sender, instance, user=None, topic=None, date_created=None, **kwargs):
	"""
	This is a generic singal for adding an object to the Topic.

	"""
	ctype = ContentType.objects.get_for_model(instance)
	obj, created = Post.objects.get_or_create(
		content_type=ctype,
		object_id=instance.id,
        defaults={
            'user': instance.user,
            'topic': instance.topic,
            'date_created': datetime.datetime.now()
            })

def delete_post_signal(sender, instance, **kwargs):
	"""
	This is a generic singal to delete related Post when an object is deleted.

	"""
	ctype = ContentType.objects.get_for_model(instance)
	try:
		post = Post.objects.get(content_type=ctype, object_id=instance.id)
		post.delete()
	except Post.MultipleObjectsReturned:
		posts = Post.objects.filter(content_type=ctype, object_id=instance.id)
		for post in posts:
			post.delete()
	except Post.DoesNotExist:
		pass

def delete_post_object_signal(sender, instance, **kwargs):
	"""
	This is a generic singal to delete related object when a Post is deleted.

	"""
	if instance.content_object:
	    instance.content_object.delete()
