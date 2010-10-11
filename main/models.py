from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):    
    user = models.ForeignKey(User, unique=True)
    points = models.IntegerField()
    
    def __unicode__(self):
        return "%s's profile" % self.user
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
        
post_save.connect(create_user_profile, sender=User)

class Room(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)

    def __unicode__(self):
		return self.name

class Question(models.Model):
    question = models.CharField(max_length=200)
    # Set to current date when object is created
    date_created = models.DateTimeField(auto_now_add=True)
    real_answer = models.CharField(max_length=100)
    author = models.ForeignKey(User)
    room = models.ForeignKey(Room)
    points = models.IntegerField()

    def __unicode__(self):
        return self.question

class Turn(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(null=True)
    user = models.ForeignKey(User)
    room = models.ForeignKey(Room)
    # Use result_set here to access associated
    # results

    def __unicode__(self):
        return '[%s] %s' % (date_start, room)

class Result(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=200, blank=True)
    turn = models.ForeignKey(Turn)

