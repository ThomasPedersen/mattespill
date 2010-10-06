# Create your views here.

from django.template import Context, loader
from django.utils import simplejson
from django.http import HttpResponse

def index(request):
	return HttpResponse("Mattespill")

def users(request):
	response = {'result': 'error', 'text': 'hore'}
	json = simplejson.dumps(response)
	return HttpResponse(json, mimetype='application/json')

def userid(request, user_id):
	t = loader.get_template('templates/userid.html')
	c = Context({
		'user_id': user_id,
	})
	return HttpResponse(t.render(c))
