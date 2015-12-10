from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from qrcode.forms import CustomUserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
	context = {
		'user': request.user
	}
	return render(request, 'qrcode/home.html', context)

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('qrcode:profile', args=()))
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)

		if form.is_valid():
			new_user = form.save(commit=True)
			# Log in that user.
			user = authenticate(username=new_user.username,
				password=form.clean_password2())
			if user is not None:
				login(request, user)
			else:
				raise Exception
			return HttpResponseRedirect(reverse('qrcode:profile', args=()))
	else:
		form = CustomUserCreationForm

	context = {
		'form': form,
	}

	return render(request, 'qrcode/register.html', context)

# Authenticated views
#####################
@login_required
def profile(request):
	'''List of recent posts by people I follow'''

	user = request.user

	context = {
		'user': user,
	}
	return render(request, 'qrcode/profile.html', context)

@login_required
def item(request, item_id):
	'''List of recent posts by people I follow'''

	user = request.user
	item = item_id # will be replaced with a model

	context = {
		'user': user,
		'item': item,
	}
	return render(request, 'qrcode/item.html', context)