from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True) # include the email field
	
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ("username", "email", "password1", "password2")
		help_texts = {
			'username' : '',
		}

	def save(self, commit=True):
		user = super(CustomUserCreationForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user