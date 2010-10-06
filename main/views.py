# Create your views here.

from django.utils import simplejson
from django.http import HttpResponse

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

def questions(request):
    question_list = Question.objects.all()    
    return HttpResponse(question_list)