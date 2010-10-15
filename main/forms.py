from django.contrib.auth.models import User
from django import forms

class SignupForm(forms.Form):
    Brukernavn = forms.CharField(max_length=30)
    Epost = forms.EmailField();
    Passord = forms.CharField(max_length=30, 
                                widget=forms.PasswordInput(render_value=False))
    Bekreft_Passord = forms.CharField(max_length=30, 
                                widget=forms.PasswordInput(render_value=False))
    Fornavn = forms.CharField(max_length=30)
    Etternavn = forms.CharField(max_length=30)
    
    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("This username is already in use")
    
    def clean(self):
        if 'password1' in self.changed_data and 'password2' in self.changed_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data
    
    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['Brukernavn'], 
                                            email=self.cleaned_data['Epost'], 
                                            password=self.cleaned_data['Passord'])
        new_user.first_name = self.cleaned_data['Fornavn']
        new_user.last_name = self.cleaned_data['Etternavn']        
        new_user.save()
        return new_user
