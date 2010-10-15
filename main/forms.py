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
            User.objects.get(username=self.cleaned_data['Brukernavn'])
        except User.DoesNotExist:
            return self.cleaned_data['Brukernavn']
        raise forms.ValidationError("Dette brukernavnet er allerede tatt.")
    
    def clean(self):
        if 'Passord' in self.changed_data and 'Bekreft_Passord' in self.changed_data:
            if self.cleaned_data['Passord'] != self.cleaned_data['Bekreft_Passord']:
                raise forms.ValidationError("Passordene er ikke like")
        return self.cleaned_data
    
    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['Brukernavn'], 
                                            email=self.cleaned_data['Epost'], 
                                            password=self.cleaned_data['Passord'])
        new_user.first_name = self.cleaned_data['Fornavn']
        new_user.last_name = self.cleaned_data['Etternavn']        
        new_user.save()
        return new_user
