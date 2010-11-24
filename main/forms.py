from django.contrib.auth.models import User, Group
from django import forms

default_errors = {
	'required': 'This field is required',
	'invalid': 'Enter a valid value'
}

class SignupForm(forms.Form):
	'''
	Class defining the signup form for creating new users
	It contains the wollowing form fields:
	- user name
	- email
	- password
	- password confirmation
	- last name
	- first name
	- class
	'''
	Brukernavn = forms.CharField(max_length=30, required=True, error_messages=default_errors)
	Epost = forms.EmailField();
	Passord = forms.CharField(max_length=30, 
								widget=forms.PasswordInput(render_value=False))
	Bekreft_Passord = forms.CharField(max_length=30, 
								widget=forms.PasswordInput(render_value=False))
	Fornavn = forms.CharField(max_length=30)
	Etternavn = forms.CharField(max_length=30)
	Klasse = forms.ModelChoiceField(queryset = Group.objects.all(), initial = Group.objects.all()[0])
	
	def clean_Brukernavn(self):
		'''
		This method makes sure that the username is not already registered,
		and returns its cleaned version.
		'''
		try:
			User.objects.get(username=self.cleaned_data['Brukernavn'])
		except User.DoesNotExist:
			return self.cleaned_data['Brukernavn']
		raise forms.ValidationError("Dette brukernavnet er allerede tatt.")
	
	def clean(self):
		'''
		This method provides additional validation.
		The password fields need to be equal.
		'''
		if 'Passord' in self.changed_data and 'Bekreft_Passord' in self.changed_data:
			if self.cleaned_data['Passord'] != self.cleaned_data['Bekreft_Passord']:
				raise forms.ValidationError("Passordene er ikke like")
		return self.cleaned_data
	
	def save(self):
		'''
		This method creates the new user from the form values that are already validated.
		'''
		new_user = User.objects.create_user(username=self.cleaned_data['Brukernavn'], 
											email=self.cleaned_data['Epost'], 
											password=self.cleaned_data['Passord'])
		new_user.first_name = self.cleaned_data['Fornavn']
		new_user.last_name = self.cleaned_data['Etternavn']	
		g = self.cleaned_data['Klasse']
		new_user.groups.add(g)
		new_user.save()
		return new_user
