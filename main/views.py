# -*- coding: utf-8 -*-

from django.template import RequestContext, Context, loader
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib.auth.models import Group
from datetime import datetime
from mattespill.main.models import Question, Room, Turn, Result, UserProfile, Hint
from mattespill.main.forms import SignupForm
from re import match
from json import dumps

login_url = '/login/'

def index(request):
	if request.user.is_authenticated():
		if request.user.get_profile().is_gameover():
			return render_to_response('game_over.html', {'user': request.user})		
		else:
			rooms = Room.objects.all()
			return render_to_response('home.html', {'user': request.user, 'home': True, \
					'rooms': rooms})
	else:
		return HttpResponseRedirect(login_url)

def room(request, room_id):
	if request.user.is_authenticated():
		if request.user.get_profile().is_gameover():
			return render_to_response('game_over.html', {'user': request.user})
		
		sess_room_id = request.session.get('room_id', None)
		if not sess_room_id or sess_room_id != room_id:
			room = get_object_or_404(Room, pk=room_id)
		else:
			room = get_object_or_404(Room, pk=sess_room_id)
	
		# If user does not have enough points to access room,
		# we redirect to index 
		if request.user.get_profile().points < room.required_points:
			return HttpResponseRedirect('/')

		request.session['room_id'] = room_id
		turn_exists = False
		try:
			t = Turn.objects.get(room=room, user=request.user, complete=False)
			turn_exists = True
		except Turn.DoesNotExist:
			t = Turn(date_start=datetime.now(), date_end=None, user=request.user, room=room)
			t.save()
			# Fetch 10 random questions for the given room (sorted by points/difficulty)
			questions = Question.objects.filter(room=room).order_by('?').order_by('points')[:10]
			# Add Result objects (question and answer pairs) for each question
			i = 1 # Sequence number for each question
			for q in questions:
				result = Result(question=q, turn=t, index=i)
				result.save()
				i += 1
		previous_turns = Turn.objects.filter(room=room, user=request.user, complete=True).\
				order_by('-date_start').order_by('-total_points').all()
		return render_to_response('room.html', {'turn_exists': turn_exists, 'turn': t, \
				'user': request.user, 'previous_turns': previous_turns})
	else:
		return HttpResponseRedirect(login_url)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

def newgame(request):
	if request.user.is_authenticated():
		if request.user.get_profile().is_gameover():
			# Delete all turns for user
			Turn.objects.filter(user=request.user).delete()
			# Reset points for user
			profile = request.user.get_profile()
			profile.points = 50
			profile.save()
		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect(login_url)

def buyhint(request):
	if request.user.is_authenticated() and request.method == 'POST':
		if request.user.get_profile().is_gameover():
			return HttpResponseForbidden
		# Get a random hint
		room_id = request.session.get('room_id', None)
		if room_id:
			hint = Hint.objects.filter(room=room_id).order_by('?')[:1]
			# Check if user has enough points
			profile = request.user.get_profile()
			cost = hint[0].cost
			if profile.points - cost <= 0:
				return HttpResponse(dumps({'points': profile.points, \
						'hint': None}), mimetype='application/json')
			else:
				profile.points -= cost
				profile.save()
				# Return json response
				return HttpResponse(dumps({'points': profile.points, 'hint': hint[0].text}), \
						mimetype='application/json')
		else:
			return HttpResponse('You must select a room before buying hints')
	else:
		return HttpResponseForbidden()

def stats(request):
	if request.user.is_authenticated():
		if request.user.get_profile().is_gameover():
			return render_to_response('game_over.html', {'user': request.user})
		# Get max 10 users ordered by points desc
		users = UserProfile.objects.order_by('-points')[:10]
		return render_to_response('stats.html', {'user': request.user, 'users': users})
	else:
		return HttpResponseRedirect(login_url)

def stats_grouped(request):
	if request.user.is_authenticated():
		if request.user.is_staff:
			stats = []
			for group in Group.objects.order_by('name').all():
				# Filtering on foreign keys awesomeness!
				stats.append((group.name, UserProfile.objects.filter(user__groups__name=group.name).order_by('-points')))
			return render_to_response('stats_grouped.html', {'user': request.user, 'stats': stats})
		else:
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect(login_url)

def question(request):
	if request.user.is_authenticated():
		if request.user.get_profile().is_gameover():
			return render_to_response('game_over.html', {'user': request.user})

		room_id = request.session.get('room_id', None)
		if room_id:
			try:
				turn = Turn.objects.get(room=room_id, user=request.user, complete=False)
			except Turn.DoesNotExist:
				return HttpResponseRedirect('/room/%s/' % room_id)
			try:
				# The Meta.ordering defined in model will sort
				# the result ascending on Result.index
				result = Result.objects.filter(turn=turn, answer='')[:1]
				if not result:
					return render_to_response('room.html', {'turn': turn, 'user': request.user})
				
				num_questions = Result.objects.filter(turn=turn).count()
				return render_to_response('question.html', {'user': request.user,'turn': turn, 'result': result[0], \
						'num_questions': num_questions, 'room_id': room_id})
			except Result.DoesNotExist:
				return HttpResponseRedirect('/room/%s/' % room_id)
	else:
		return HttpResponseRedirect(login_url)

def answer(request):
	if request.user.is_authenticated() and request.method == 'POST':
		if request.user.get_profile().is_gameover():
			return HttpResponseForbidden()
		
		room_id = request.session.get('room_id', None)
		if room_id and 'answer' in request.POST:
			given_answer = request.POST['answer'].strip()
			
			# Check if given_answer is a number
			if match('^-?\d+$', given_answer) == None:
				return HttpResponseBadRequest()
			
			turn = get_object_or_404(Turn, room=room_id, user=request.user, complete=False)
			count = Result.objects.filter(turn=turn).count()
			result = Result.objects.filter(turn=turn, answer='')[0]
			profile = request.user.get_profile()
			try:	
				if result.index < count:
					index = result.index + 1
					question = Result.objects.get(turn=turn, index=index).question.question
				else:
					index = -1 # No more questions
					question = None
					turn.complete = True
					turn.save()
				correct = given_answer == result.question.real_answer
				earned = None
				lost = None
				if correct:
					# Give user some points
					profile.points += result.question.points
					turn.total_points += result.question.points
					earned = result.question.points
				else:
					# For wrong answer users lose (question points / 2)
					penalty = result.question.points / 2
					diff = profile.points - penalty
					if diff <= 0:
						profile.points = 0
					else:
						profile.points -= penalty
					turn.total_points -= penalty
					lost = penalty
				turn.save()
				profile.save()
				result.answer = given_answer
				result.save()
				return HttpResponse(dumps({'correct': correct, 'index': index, \
						'question': question, 'points': profile.points, 'earned': earned, \
						'lost': lost}), mimetype='application/json')
			except Result.DoesNotExist as e:
				return HttpResponseServerError(e)
	else:
		return HttpResponseRedirect(login_url)


def signup(request):
	if request.user.is_authenticated():
		if request.user.is_staff:
			if request.method == 'POST':
				form = SignupForm(data=request.POST)
				if form.is_valid():
					form.save();
					return HttpResponseRedirect('/manage/')
			form = SignupForm()
			return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/')
	else:
			return HttpResponseRedirect(login_url)
		
def game_over(request):
	if request.user.is_authenticated():
		if not request.user.get_profile().is_gameover():
			return HttpResponseRedirect('/')
		return render_to_response('game_over.html', {'user': request.user})
	else:
		return HttpResponseRedirect(login_url)

def manage(request):
	if request.user.is_authenticated():
		if request.user.is_staff:
			return render_to_response('manage.html', { 'user': request.user })
		else:
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect(login_url)

