from django.test import TestCase
from django.test.client import Client
from main.models import Turn 
from json import loads

class ViewsTest(TestCase):

	def test_login(self):
		response = self.client.post('/login/', {'username': 'foo', 'password': 'foo'})
		self.assertEqual(response.status_code, 302)
		response = self.client.post('/login/', {'username': 'invaliduser', 'password': \
				'invalidpassword'})
		self.assertEqual(response.status_code, 200)

	def test_index(self):
		# Should redirect if we're not logged in
		response = self.client.get('/')
		self.assertEqual(response.status_code, 302)
		# Log in
		self.client.login(username='foo', password='foo')
		# Get index
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_room(self):
		# No auth should result in redirect
		response = self.client.get('/room/1/')
		self.assertEqual(response.status_code, 302)
		# Log in
		self.client.login(username='foo', password='foo')
		# User foo does not have enough points to access this room
		response = self.client.get('/room/2/')
		self.assertEqual(response.status_code, 302)
		# ..should be enough for this room though
		response = self.client.get('/room/1/')
		self.assertEqual(response.status_code, 200)
		# Session should now contain the room id
		session = self.client.session
		self.assertEqual(session['room_id'], '1')
		# Check if a turn was created
		turns = Turn.objects.filter(user=1)
		self.assertEqual(turns.count(), 1)
		# Check if turn contains atleast one Result object
		self.assertTrue(turns[0].result_set.count() > 1)

	def test_buyhint(self):
		# Log in
		self.client.login(username='foo', password='foo')
		response = self.client.get('/room/1/')
		self.assertEqual(response.status_code, 200)
		# Buy hint
		response = self.client.post('/buyhint/')
		from_json = loads(response.content)
		self.assertNotEqual(from_json['hint'], None)
		# Buy another hint (should return None since user does not have enough points)
		response = self.client.post('/buyhint/')
		from_json = loads(response.content)
		self.assertEqual(from_json['hint'], None)

