from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):	
	'''Class defining the UserProfile model'''
	user = models.ForeignKey(User, unique=True)
	points = models.IntegerField(default=50, null=True)

	def __unicode__(self):
		return "%s's profile" % self.user

	def groups(self):
		'''Returns all groups this user's a member of'''
		return self.user.groups.all()

	def is_gameover(self):
		return self.points <= 0

def create_user_profile(sender, instance, created, **kwargs):
	'''Creates user profile'''
	if created:
		profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)

class Room(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=300)
	required_points = models.IntegerField()

	def __unicode__(self):
		return self.name

class Hint(models.Model):
	text = models.TextField()
	cost = models.IntegerField(default=0)
	room = models.ForeignKey(Room)

	def __unicode__(self):
		return '[%s] %s' % (self.room, self.text)

class Question(models.Model):
	question = models.CharField(max_length=200)
	# Set to current date when object is created
	date_created = models.DateTimeField(auto_now_add=True)
	real_answer = models.CharField(max_length=100)
	author = models.ForeignKey(User)
	room = models.ForeignKey(Room)
	points = models.IntegerField()

	def __unicode__(self):
		return '[%s] %s' % (self.room, self.question)

class Turn(models.Model):
	date_start = models.DateTimeField()
	date_end = models.DateTimeField(null=True)
	user = models.ForeignKey(User)
	room = models.ForeignKey(Room)
	complete = models.BooleanField(default=False)
	total_points = models.IntegerField(default=0)
	# Use result_set here to access associated
	# results

	def __unicode__(self):
		return '[%s, %s] %s' % (self.room, self.date_start.strftime('%Y-%m-%d %H:%M:%S'), self.user.username)

class Result(models.Model):
	index = models.IntegerField()
	question = models.ForeignKey(Question)
	answer = models.CharField(max_length=200, blank=True)
	turn = models.ForeignKey(Turn)
	# Order by index field
	class Meta:
		ordering = ('index', )
