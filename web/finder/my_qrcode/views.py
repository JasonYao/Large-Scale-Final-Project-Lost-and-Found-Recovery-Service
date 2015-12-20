from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from my_qrcode.models import Item, FinderUser
from my_qrcode.forms import CustomUserCreationForm, ItemForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from qrcode import * # needs Python Image Library (PIL)
from django.conf import settings

# helper functions
def createFinderUser(user):
	u = FinderUser(
		user_id=user.id, username=user.username, 
		email=user.email)
	u.save()

def generate_item_id():
	last_item = Item.objects.all().order_by('-pk')
	if len(last_item) > 0:
		return last_item[0].item_id + 1
	return 1

# Create your views here.

def index(request):
	user = None
	if request.user:
		user = request.user
	context = {
		'user': user
	}
	return render(request, 'my_qrcode/home.html', context)

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('my_qrcode:profile', args=()))
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
			return HttpResponseRedirect(reverse('my_qrcode:profile', args=()))
	else:
		form = CustomUserCreationForm

	context = {
		'form': form,
	}

	return render(request, 'my_qrcode/register.html', context)

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

	items = Item.objects.filter(owner=finderUser)

	context = {
		'user': user,
		'items': items,
	}
	return render(request, 'my_qrcode/profile.html', context)

def item(request, user_id, item_id):
	'''List of recent posts by people I follow'''

	user = FinderUser.objects.get(user_id=user_id)
	item = Item.objects.get(item_id=item_id)

	context = {
		'user': user,
		'item': item,
	}
	return render(request, 'my_qrcode/item.html', context)

@login_required
def add_item(request):
	'''List of recent posts by people I follow'''

	user = FinderUser.objects.get(user_id=request.user.id)

	if request.method == 'POST':
		form = ItemForm(request.POST)

		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.owner = user
			new_item.status = Item.ITEM_NOT_LOST

			# set item id
			item_id = generate_item_id()

			while len(Item.objects.filter(item_id=item_id)):
				item_id = generate_item_id()

			new_item.item_id = item_id

			new_item.save()

			return HttpResponseRedirect(reverse('my_qrcode:profile', args=()))
	else:
		form = ItemForm

	context = {
		'user': user,
		'form': form,
	}
	return render(request, 'my_qrcode/item_add.html', context)

@login_required
def edit_item(request, item_id):
	'''List of recent posts by people I follow'''

	user = FinderUser.objects.get(user_id=request.user.id)
	item = get_object_or_404(Item, item_id=item_id)

	if item.owner != user:
		return HttpResponseForbidden()

	if request.method == 'POST':
		form = ItemForm(request.POST, instance=item)

		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.save()
			return HttpResponseRedirect(reverse('my_qrcode:profile', args=()))
	else:
		form = ItemForm(instance=item, initial={'mark_lost': (item.status == Item.ITEM_LOST),})

	context = {
		'user': user,
		'form': form,
		'item_id': item_id,
	}
	return render(request, 'my_qrcode/item_edit.html', context)

@login_required
def delete_item(request, item_id):
	'''List of recent posts by people I follow'''

	user = FinderUser.objects.get(user_id=request.user.id)
	item = get_object_or_404(Item, item_id=item_id)

	if item.owner != user:
		return HttpResponseForbidden()

	if request.method == 'POST':
		item.delete()    	
		return HttpResponseRedirect(reverse('my_qrcode:profile', args=()))

	context = {
		'user': user,
		'item': item,
	}
	return render(request, 'my_qrcode/item_delete.html', context)

@login_required
def generate(request, item_id):

	user = FinderUser.objects.get(user_id=request.user.id)
	item = get_object_or_404(Item, item_id=item_id)

	if item.owner != user:
		return HttpResponseForbidden()

	# this is where we'll create the qrcode
	qr_url = '/found/' + str(user.user_id) + '/' + str(item_id) + '/' # make this the full site url, for now leave it as this dummy url
	qr_uri = request.build_absolute_uri(qr_url) # the full absolute uri to be sent to the qrcode app

	# generate the qr_code
	

	context = {
		'user': user,
		'item_id': item_id,
		'qr_url': qr_uri,
	}
	return render(request, 'my_qrcode/generate.html', context)

def found(request, user_id, item_id):

	user = FinderUser.objects.get(user_id=user_id)
	item = get_object_or_404(Item, item_id=item_id)

	if item.owner != user:
		return HttpResponseForbidden()

	# mark the item as found here
	if item.status == Item.ITEM_LOST:
		item.status = Item.ITEM_FOUND

	context = {
		'user': user,
		'item': item,
	}
	return render(request, 'my_qrcode/found.html', context)