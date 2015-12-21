from django import forms
from django.forms import ModelForm, TextInput, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from my_qrcode.models import Item

class CustomUserCreationForm(UserCreationForm):
	#email = forms.EmailField(required=True) # include the email field
	username = forms.CharField(label="", help_text="", required=True, widget=forms.TextInput(attrs={'placeholder': 'Username',}))
	email = forms.EmailField(label="", help_text="", required=True, widget=forms.TextInput(attrs={'type': 'email', 'placeholder': 'Email',}))
	password1 = forms.CharField(label="", help_text="", required=True, widget=PasswordInput(attrs={'placeholder': 'Password',}))
	password2 = forms.CharField(label="", help_text="", required=True, widget=PasswordInput(attrs={'placeholder': 'Confirm Password',}))
	
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ("username", "email", "password1", "password2")
		help_texts = {
			'username' : '',
		}

	def clean_email(self):
		email = self.cleaned_data['email']
		username = self.cleaned_data['username']
		if email and User.objects.filter(email=email).exclude(username=username).count():
			raise forms.ValidationError(u'Email addresses must be unique.')
		return email

	def save(self, commit=True):
		user = super(CustomUserCreationForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user

class ItemForm(ModelForm):
  mark_lost = forms.BooleanField(label='Mark Item Lost?', required=False)
  
  class Meta:
    model = Item
    fields = ('name', 'is_public', 'mark_lost',)
    widgets = {
      'name': TextInput(attrs={'id' : 'input_item'}),
    }

  def clean_mark_lost(self):
  	lost = self.cleaned_data['mark_lost']
  	return lost

  def save(self, commit=True):
  	item = super(ItemForm, self).save(commit=False)
  	lost = self.cleaned_data['mark_lost']

  	if lost:
  		item.status = Item.ITEM_LOST
  	elif item.status != Item.ITEM_FOUND:
  		item.status = Item.ITEM_NOT_LOST

  	if commit:
  		item.save()

  	return item

