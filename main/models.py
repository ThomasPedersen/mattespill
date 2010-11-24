from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def create_user_profile(sender, instance, created, **kwargs):
	'''Method to create user profile'''
	if created:
		profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)



class UserProfile(models.Model):
	'''
	Class defining the UserProfile model.
	This class contains the user's points as well as it's django User object,
	used for authentication
	'''
	user = models.ForeignKey(User, unique=True)
	points = models.IntegerField(default=50, null=True)

	def __unicode__(self):
		return "%s's profile" % self.user

	def groups(self):
		'''Returns all groups this user is a member of'''
		return self.user.groups.all()

	def is_gameover(self):
		'''Returns true if the game is over for this user'''
		return self.points <= 0

class Room(models.Model):
	'''
	This class represents a room. ( + - * / )
	Contains room name, description, and number of points required to enter the room
	'''
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=300)
	required_points = models.IntegerField()

	def __unicode__(self):
		return self.name

class Hint(models.Model):
	'''
	This class represents a hint, which is a short, general message gived in
	a certain room.
	Each hint has a cost associated with it,
	and contains a multiline text
	'''
	text = models.TextField()
	cost = models.IntegerField(default=0)
	room = models.ForeignKey(Room)

	def __unicode__(self):
		return '[%s] %s' % (self.room, self.text)

class Question(models.Model):
	'''
	This class represents a question, which belongs to a room.
	A reference to author who wrote it is stored, as well as
	the room in which the question should appear,
	the amount of points it rewards, the date it was added,
	a text field with the question itself
	and a text field with its correct answer
	'''
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
	'''
	This class represents a turn which is created everytime a user starts a round of
	questions in a room.
	It contains:
	- a date which is when the turn started
	- a date which is when the turn ended, if it has yet ended
	- the user which this turn represents
	- a boolean describing wether the turn has ended
	- the total number of points accumulated during this turn
	'''
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
	'''
	This class represents the result of a question submitted by a user.
	It contains:
	- a unique integer index
	- a reference to which question this result answers
	- a string containing the answer itself
	- the turn in which this result was answered
	'''
	index = models.IntegerField()
	question = models.ForeignKey(Question)
	answer = models.CharField(max_length=200, blank=True)
	turn = models.ForeignKey(Turn)

	# Order by index field
	class Meta:
		'''Specify that the results should be ordered by their index when selected'''
		ordering = ('index', )
