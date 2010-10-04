from django.db import models

class Group(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class User(models.Model):
	access = models.IntegerField()
	username = models.CharField(max_length=40)
	password = models.CharField(max_length=32) # MD5 hash
	group = models.ManyToManyField(Group)

	def __unicode__(self):
		return self.username

class Room(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
	 return self.name

class Task(models.Model):
	question = models.CharField(max_length=200)
	date = models.DateTimeField()
	answer = models.CharField(max_length=100)
	author = models.ForeignKey(User)
	room = models.ForeignKey(Room)

	def __unicode__(self):
		return self.question

class Result(models.Model):
	user = models.ForeignKey(User)
	task = models.ForeignKey(Task)
	turn = models.IntegerField()
	date_start = models.DateTimeField()
	date_end = models.DateTimeField()

	def __unicode__(self):
		return self.user

class Answer(models.Model):
	result = models.ForeignKey(Result)
	answer = models.CharField(max_length=200)

	def __unicode__(self):
		return self.answer


