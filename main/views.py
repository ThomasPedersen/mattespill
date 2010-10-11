# -*- coding: utf-8 -*-

from django.template import Context, loader
from django.utils import simplejson
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from datetime import datetime
from mattespill.main.models import Question, Room, Turn, Result

login_url = '/login/'

def index(request):
	if request.user.is_authenticated():
		request.user.profile = request.user.get_profile()
		return render_to_response('home.html', {'user': request.user, 'profile': request.user.get_profile()})
	else:
		return HttpResponseRedirect(login_url)

def room(request, room_id):
	if request.user.is_authenticated():
		turn_id = request.session.get('turn_id', None)
		# Create a new Turn if none currently exists
		if not turn_id:
			r = get_object_or_404(Room, pk=room_id)
			t = Turn(date_start=datetime.now(), date_end=None, user=request.user, room=r)
			t.save()
            # Fetch 10 questions for the given room
			questions = Question.objects.filter(room=r)[:10]
            # Add Result objects (question, answer pairs) for each question
			for q in questions:
				result = Result(question=q, turn=t)
				result.save()
			# And finally set the session key for turn_id
			request.session['turn_id'] = t.id
		else:
			t = get_object_or_404(Turn, pk=turn_id)
		return render_to_response('room.html', {'turn': t})
	else:
		return HttpResponseRedirect(login_url)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

def users(request):
	response = {'result': 'error', 'text': 'hore'}
	json = simplejson.dumps(response)
	return HttpResponse(json, mimetype='application/json')

def userid(request, user_id):
	if int(user_id) > 10:
		return HttpResponse('User above 10 -> Nr: %s.' % user_id)
	else:
		return HttpResponse('User below or 10 -> Nr: %s' % user_id)

def questions(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render_to_response('question.html', {'question': q})

def answer(request, result_id):
    if request.user.is_authenticated():
        # If the user hasn't started his turn yet, we create a new
        # Turn object and populate it with questions
        if request.session.get('turn_id', None):
			t = Turn(date_start=datetime.now(), date_end=None, user=request.user, room=None)
        r = get_object_or_404(Result, pk=result_id)
        return render_to_respone('answer.html', {'result': q})

