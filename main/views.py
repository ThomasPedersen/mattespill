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
import logging

login_url = '/login/'

def index(request):
	if request.user.is_authenticated():
		return render_to_response('home.html', {'user': request.user })
	else:
		return HttpResponseRedirect(login_url)

def room(request, room_id):
	if request.user.is_authenticated():
		sess_room_id = request.session.get('room_id', None)
		if not sess_room_id or sess_room_id != room_id:
			room = get_object_or_404(Room, pk=room_id)
		else:
			room = get_object_or_404(Room, pk=sess_room_id)
		request.session['room_id'] = room_id
		try:	
			t = Turn.objects.get(room=room, user=request.user)
		except Turn.DoesNotExist:
			t = Turn(date_start=datetime.now(), date_end=None, user=request.user, room=room)
			t.save()
			# Fetch 10 questions for the given room
			questions = Question.objects.filter(room=room)[:10]
			# Add Result objects (question, answer pairs) for each question
			for q in questions:
				result = Result(question=q, turn=t)
				result.save()
		else:
			t = get_object_or_404(Turn, room=room, user=request.user)
		return render_to_response('room.html', {'turn': t, 'user': request.user})
	else:
		return HttpResponseRedirect(login_url)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

def questions(request, question_id):
	q = get_object_or_404(Question, pk=question_id)
	return render_to_response('question.html', {'question': q})

def answer(request, room_id, result_id):
	if request.user.is_authenticated():
		# If the user hasn't started his turn yet, we create a new
		# Turn object and populate it with questions
		if request.session.get('room_id', None):
			r = get_object_or_404(Room, pk=room_id)
			t = get_object_or_404(Turn, room=r, user=request.user)
		return render_to_respone('answer.html', {'result': q})

