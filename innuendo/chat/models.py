from django.db import models

# Create your models here.
class User(models.Model):
	first_name = models.CharField(max_length = 20)
	last_name = models.CharField(max_length = 20)
	color = models.CharField(max_length = 6)   # hexadecimal representation

	def __str__(self):
		return self.first_name + " " + self.last_name

	def __eq__(self, other):
		return self.first_name == other.first_name and self.last_name == other.last_name

class Message(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	text = models.CharField(max_length = 200)
	timestamp = models.DateTimeField("time of message")

	def __str__(self):
		return str(self.user) + ": " + self.text

class Group(models.Model):
	message = models.ForeignKey(Message, on_delete = models.CASCADE)