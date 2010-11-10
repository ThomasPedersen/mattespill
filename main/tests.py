from django.test import TestCase
from django.test.client import Client
from main.models import Turn, UserProfile
from json import loads

class ViewsTest(TestCase):

	def test_login(self):
		# Login, redirects on success
		response = self.client.post('/login/', {'username': 'foo', 'password': 'foo'})
		self.assertEqual(response.status_code, 302)
		# Invalid login, refreshes on login
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

	def test_newgame(self):
		# Log in
		self.client.login(username='foo', password='foo')
		# Try calling new game without being game over (should not reset points)
		profile = UserProfile.objects.get(user__username='foo')
		current_points = profile.points
		response = self.client.get('/newgame/')
		self.assertEqual(response.status_code, 302)
		self.assertEqual(current_points, profile.points)
		# Remove foo's points
		profile.points = 0
		profile.save()
		self.assertEqual(profile.points, 0)
		# Profile should now be game over
		self.assertTrue(profile.is_gameover())
		# Reset game
		response = self.client.get('/newgame/')
		self.assertEqual(response.status_code, 302)
		# Refetch profile and compare points (should now be reset to 50)
		profile = UserProfile.objects.get(user__username='foo')
		self.assertEqual(profile.points, 50)
		# Verify that all Turns for foo has been deleted
		self.assertEqual(Turn.objects.filter(user__username='foo').count(), 0)

	def test_answer(self):
		# Log in
		self.client.login(username='foo', password='foo')
		# Start a turn
		response = self.client.get('/room/1/')
		# Answer question (non-numeric answer, should fail with bad request)
		response = self.client.post('/answer/', {'answer': 'sdf'})
		self.assertEqual(response.status_code, 400)
		# Send correct answer (ok, this is cheating...)
		real_answer = Turn.objects.filter(user__username='foo')[0].result_set.all()[0].question.real_answer
		response = self.client.post('/answer/', {'answer': real_answer})
		self.assertEqual(response.status_code, 200)
		# Incorrect answer (numeric, should be successful)
		response = self.client.post('/answer/', {'answer': 42})
		self.assertEqual(response.status_code, 200)
	
