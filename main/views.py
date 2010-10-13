# -*- coding: utf-8 -*-

from django.template import Context, loader
from django.utils import simplejson
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core import serializers
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
			# Add Result objects (question and answer pairs) for each question
			i = 1 # Sequence number for each question
			for q in questions:
				result = Result(question=q, turn=t, index=i)
				result.save()
				i += 1
		return render_to_response('room.html', {'turn': t, 'user': request.user})
	else:
		return HttpResponseRedirect(login_url)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

def question(request):
	if request.user.is_authenticated():
		room_id = request.session.get('room_id', None)
		if room_id:
			t = get_object_or_404(Turn, room=room_id, user=request.user)
			try:
				# The Meta.ordering defined in model will sort
				# the result ascending on Result.index
				r = Result.objects.filter(turn=t, answer='')[:1]
				return HttpResponse(serializers.serialize('json', (r[0].question, ), fields=('question')))
			except Result.DoesNotExist:
				pass

def cur_question(request):
	if request.user.is_authenticated():
		room_id = request.session.get('room_id', None)
		if room_id:
			r = get_object_or_404(Room, pk=room_id)
			t = get_object_or_404(Turn, room=r, user=request.user)
			try:
				result = Result.objects.filter(turn=t, answer='')[:1]
				num_questions = Result.objects.filter(turn=t).count()
				return render_to_response('question.html', {'user': request.user,'turn': t, 'result': result[0], 'num_questions': num_questions})
			except Turn.DoesNotExist:
				pass

def answer(request, result_id):
	if request.user.is_authenticated():
		room_id = request.session.get('room_id', None)
		if room_id:
			#r = get_object_or_404(Room, pk=room_id)
			#t = get_object_or_404(Turn, room_id=room_id, user=request.user)
			#r = get_object_or_404(Result, pk=result_id)
			#r.answer = request.POST['answer']
			#r.save()
			pass

