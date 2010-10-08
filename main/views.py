# -*- coding: utf-8 -*-

from django.template import Context, loader
from django.utils import simplejson
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from mattespill.main.models import Question

def index(request):
	if request.user.is_authenticated():
		return render_to_response('home.html', {'user': request.user.username})
	else:
		return HttpResponseRedirect("/login/")

'''def login(request):
	if request.method == 'POST': 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is None:
			return render_to_response('error.html', {'message' : 'Du har enten skrevet feil brukernavn eller passord, eller brukeren din er ikke registrert. Kontakt lærer'})
		else:
			if user.is_active:
				login(request, user)
			# Redirect to a success page.
			else:
				return render_to_response('error.html', {'message' : 'Din konto er deaktivert. Kontakt lærer'})
	else:
		return render_to_response('login.html')'''

def users(request):
	response = {'result': 'error', 'text': 'hore'}
	json = simplejson.dumps(response)
	return HttpResponse(json, mimetype='application/json')

def userid(request, user_id):
	if int(user_id) > 10:
		return HttpResponse("User above 10 -> Nr: %s." % user_id)
	else:
		return HttpResponse("User below or 10 -> Nr: %s" % user_id)

def questions(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render_to_response('question.html', {'question': q})
