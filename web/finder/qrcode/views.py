from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from qrcode.models import Item, FinderUser
from qrcode.forms import CustomUserCreationForm, ItemForm
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
			# Create a mirror sharded User model.
			u = FinderUser(
				user_id=new_user.id, username=new_user.username, 
				email=new_user.email)
			u.save()
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
	items = Item.objects.filter(user_id=user.id)

	context = {
		'user': user,
		'items': items,
	}
	return render(request, 'qrcode/profile.html', context)

def item(request, user_id, item_id):
	'''List of recent posts by people I follow'''

	user = FinderUser.objects.get(user_id=user_id)
	item = Item.objects.get(item_id=item_id)

	context = {
		'user': user,
		'item': item,
	}
	return render(request, 'qrcode/item.html', context)

@login_required
def add_item(request):
	'''List of recent posts by people I follow'''

	user = request.user

	if request.method == 'POST':
		form = ItemForm(request.POST)

		if form.is_valid():
			new_item = form.save(commit=False)
    		new_item.user_id = request.user.id
    		
    		new_item.save()

    		return HttpResponseRedirect(reverse('qrcode:profile', args=()))
	else:
		form = ItemForm

	context = {
		'user': user,
		'form': form,
	}
	return render(request, 'qrcode/item_add.html', context)