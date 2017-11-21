from django.db import models

from django.db import models
import datetime

# Create your models here.

class Blog(models.Model):
	subject = models.CharField(max_length=100)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add = True)
	last_modified = models.DateTimeField(auto_now = True)

	def get_json(self):
		time_frmt = '%c'
		d = {
			'content': self.content,
			'subject': self.subject,
			'created': self.created.strftime(time_frmt),
			'last_modified': self.last_modified.strftime(time_frmt)
		}
		return d

