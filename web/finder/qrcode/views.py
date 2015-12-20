from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from qrcode.models import Item, FinderUser
from qrcode.forms import CustomUserCreationForm, ItemForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden

# helper functions
def createFinderUser(user):
	u = FinderUser(
		user_id=user.id, username=user.username, 
		email=user.email)
	u.save()

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
			createFinderUser(new_user)
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

	# TODO: a FinderUser is not created when a super user is created, so we always make one for the user here
	try:
		finderUser = FinderUser.objects.get(user_id=user.id)
	except FinderUser.DoesNotExist:
		createFinderUser(user)

	items = Item.objects.filter(user_id=user.id)

	context = {
		'user': user,
		'items': items,
	}
	return render(request, 'qrcode/profile.html', context)

def item(request, user_id, item_id):
	'''List of recent posts by people I follow'''

	user = FinderUser.objects.get(user_id=user_id)
	item = Item.objects.get(id=item_id)

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

@login_required
def edit_item(request, item_id):
	'''List of recent posts by people I follow'''

	user = request.user
	item = get_object_or_404(Item, id=item_id)

	if item.user_id != user.id:
		return HttpResponseForbidden()

	if request.method == 'POST':
		form = ItemForm(request.POST, instance=item)

		if form.is_valid():
			new_item = form.save(commit=False)
    		new_item.save()

    		return HttpResponseRedirect(reverse('qrcode:profile', args=()))
	else:
		form = ItemForm(instance=item)

	context = {
		'user': user,
		'form': form,
		'item_id': item_id,
	}
	return render(request, 'qrcode/item_edit.html', context)

@login_required
def generate(request, item_id):

	user = request.user
	item = get_object_or_404(Item, id=item_id)

	if item.user_id != user.id:
		return HttpResponseForbidden()

	# this is where we'll create the qrcode
	qr_url = '/items/' + str(item_id) + '/' # make this the full site url, for now leave it as this dummy url

	context = {
		'user': user,
		'item_id': item_id,
		'qr_url': qr_url,
	}
	return render(request, 'qrcode/generate.html', context)