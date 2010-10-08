# Create your views here.

from django.template import Context, loader
from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from mattespill.main.models import Question

def index(request):
	return HttpResponse("Mattespill")

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
