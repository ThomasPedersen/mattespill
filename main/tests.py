from django.test import TestCase
from django.test.client import Client

class ViewsTest(TestCase):

	def test_index(self):
		# Should redirect if we're not logged in
		response = self.client.get('/')
		self.failUnlessEqual(response.status_code, 302)
		# Log in
		response = self.client.post('/login/', {'username': 'testuser', 'password': 'testuser'})
		self.failUnlessEqual(response.status_code, 302) # Redirects on success
		# Get index
		response = self.client.get('/')
		self.failUnlessEqual(response.status_code, 200)

	def test_login(self):
		response = self.client.post('/login/', {'username': 'testuser', 'password': 'testuser'})
		self.failUnlessEqual(response.status_code, 302)

