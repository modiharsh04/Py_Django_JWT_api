from django.db import models
from django.conf import settings
import datetime

# Create your models here.

class Blog(models.Model):
	subject = models.CharField(max_length=100)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add = True)
	last_modified = models.DateTimeField(auto_now = True)
	author = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.CASCADE,
			default= 1
		)

	def __str__(self):
		return self.subject

	def get_author(self,usr):
		d = {
			'username' : usr.get_username()
		}
		return d

	def get_json(self):
		time_frmt = '%c'
		d = {
			'id': self.pk,
			'content': self.content,
			'subject': self.subject,
			'created': self.created.strftime(time_frmt),
			'last_modified': self.last_modified.strftime(time_frmt),
			'author' : self.get_author(self.author)
		}
		return d

