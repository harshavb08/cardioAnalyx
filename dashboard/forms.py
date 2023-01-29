from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


attr = {'class': 'form-control form-control-user'}
class SignupForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email', 'first_name', 'last_name', 'password1', 'password2']
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control form-control-user border border-primary', 'placeholder':'Nom d\'utilisateur'}), 
			'email': forms.TextInput(attrs={'class': 'form-control form-control-user border border-primary', 'placeholder':'Email'}), 
			'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user border border-primary', 'placeholder':'Prenom'}), 
			'last_name': forms.TextInput(attrs={'class': 'form-control form-control-user border border-primary', 'placeholder':'Nom'}), 
		}
	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].required = True
		self.fields['last_name'].required = False
		self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control form-control-user'})
		self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control form-control-user'})

		# for it in self.fields:
		# 	self.fields[it].error_messages['required'] = 'Cet champ est obligatoire'
		# 	if it == "password2":
		# 		self.fields[it].error_messages['password_too_short'] = "Veuillez choisir un mot de passe > 7 caractèreres "
		# 	if it == "email":
		# 		self.fields[it].error_messages['invalid'] = 'Veuillez verifier votre addresse email'
		# self.error_messages['password_mismatch'] = "Les deux mots de passe correspondent pas"
		# self.error_messages['password_too_short'] = "Veuillez choisir un mot de passe > 7 caractèreres "

class LoginForm(AuthenticationForm):
	class Meta:
		model = User
		fields = ['username','password']

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control form-control-user text_input', 'autocomplete': 'off', 'placeholder': ''})
		self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control form-control-user text_input', 'autocomplete': 'off', 'placeholder': ''})
		

		for it in self.fields:
			self.fields[it].error_messages['required'] = 'Cet champ est obligatoire'
			if it == "password":
				self.fields[it].error_messages['password_too_short'] = "Veuillez choisir un mot de passe > 7 caractèreres "
			if it == "email":
				self.fields[it].error_messages['invalid'] = 'Veuillez verifier votre addresse email'
		#self.error_messages['invalid_login'] = "Authentification echoué, verifier vos identifiants."
		self.error_messages['inactive'] = "Votre compte à été désactivé."


class ProfileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


