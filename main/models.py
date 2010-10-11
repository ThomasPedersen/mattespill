from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):    
    user = models.ForeignKey(User, unique=True)
    points = models.IntegerField()
    
    def __str__(self):
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

    def __unicode__(self):
        return self.question

class Report(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return '[%s] %s' % (date_end, user)

class Result(models.Model):
    # Assuming a set of questions are to be generated randomly
    # each turn, we need to maintain an index here so that
    # results can be sorted
    question_index = models.IntegerField()
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=200)
    report = models.ForeignKey(Report)

    def __unicode__(self):
        return self.user

