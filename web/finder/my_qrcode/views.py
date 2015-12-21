from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from my_qrcode.models import Item, FinderUser
from my_qrcode.forms import CustomUserCreationForm, ItemForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
import qrcode # needs Python Image Library (PIL)
from django.conf import settings
from utils.hints import set_user_for_sharding
from routers import bucket_users_into_shards
from django.core.cache import caches #, cache
from django.db.models.signals import post_save
from django.dispatch import receiver

# helper functions
def createFinderUser(user):
	u = FinderUser(user_id=user.id, username=user.username, email=user.email)
	u.save()

def generate_item_id(user_id):
	# avash: why do we grab all items instead of just one, limit 1
	# TODO: Fix! Check all items in all shards or keep last item id 
	# so that we can increment it, unless that doesn't matter
	last_item = Item.objects.all().order_by('-pk')
	if len(last_item) > 0:
		return last_item[0].item_id + 1
	return 1

def flashHomeMessage(request, message):
	return index(request, message)

# update cache once the model is saved
@receiver(post_save, sender=FinderUser, dispatch_uid="update_finderuser_cache_event")
def update_finderuser_cache(sender, instance, **kwargs):
	cache = caches['users']
	user_cache_key = 'qr_user_' + str(instance.user_id)
	cache.set(user_cache_key, instance)

@receiver(post_save, sender=Item, dispatch_uid="update_item_cache_event")
def update_item_cache(sender, instance, **kwargs):
	cache = caches['items']
	item_cache_key = 'qr_item_' + str(instance.item_id)
	cache.set(item_cache_key, instance)

# Create your views here.

def index(request, message = None):
	user = None
	if request.user:
		user = request.user

	context = {
		'user': user,
		'message': message,
	}
	return render(request, 'my_qrcode/home.html', context)	


def public_profile(request, parameter_user_id):
	cache = caches['users']
	user_cach_key = 'qr_user_' + str(parameter_user_id)

	try:
		request_user = request.user
		if request_user == None:
			# Requesting user is not logged in, will always return public profile views

			# query user shards
			user = cache.get(user_cach_key)
			if user is None:
				# get user from shard
				user_query = FinderUser.objects
				set_user_for_sharding(user_query, parameter_user_id)
				user = user_query.get(user_id=parameter_user_id)

				cache.set(user_cach_key, user)
			else:
				print 'User is in the cache'

			# query items shards
			item_query = Item.objects
			set_user_for_sharding(item_query, parameter_user_id)
			items = item_query.filter(owner=user)
			context = {
				'user': user,
				'items': items,
			}
			return render(request, 'my_qrcode/public_profile.html', context)
		else:
			# Requesting user is checking their own profile, allowed to edit
			if request_user.id == parameter_user_id:
				# User was matched, shown admin-rights profile page

				# query user shards
				user = cache.get(user_cach_key)
				if user is None:
					# get user from shard
					user_query = FinderUser.objects
					set_user_for_sharding(user_query, parameter_user_id)
					user = user_query.get(user_id=parameter_user_id)

					cache.set(user_cach_key, user)
				else:
					print 'User is in the cache'

				# query items shards
				item_query = Item.objects
				set_user_for_sharding(item_query, parameter_user_id)
				items = item_query.filter(owner=user)
				context = {
					'user': user,
					'items': items,
				}
				return render(request, 'my_qrcode/profile.html', context)
			else:
				# query user shards
				user = cache.get(user_cach_key)
				if user is None:
					# get user from shard
					user_query = FinderUser.objects
					set_user_for_sharding(user_query, parameter_user_id)
					user = user_query.get(user_id=parameter_user_id)

					cache.set(user_cach_key, user)
				else:
					print 'User is in the cache'

				# query items shards
				item_query = Item.objects
				set_user_for_sharding(item_query, parameter_user_id)
				items = item_query.filter(owner=user)
				context = {
					'user': user,
					'items': items,
				}
				return render(request, 'my_qrcode/public_profile.html', context)
	except FinderUser.DoesNotExist or UnboundLocalError:
		return flashHomeMessage(request, 'Sorry, we could\'t find a user by that specification')


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
			user = authenticate(username=new_user.username, password=form.clean_password2())
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
	user = request.user

	# TODO: a FinderUser is not created when a super user is created, 
	# so we always make one for the user here
	cache = caches['users']
	user_cach_key = 'qr_user_' + str(user.id)
	finderUser = cache.get(user_cach_key)
	if finderUser is None:
		try:
			# get user from shard
			user_query = FinderUser.objects
			set_user_for_sharding(user_query, user.id)
			finderUser = user_query.get(user_id=user.id)
		except FinderUser.DoesNotExist:
			createFinderUser(user)
			# get user from shard
			user_query = FinderUser.objects
			set_user_for_sharding(user_query, user.id)
			finderUser = user_query.get(user_id=user.id)

		cache.set(user_cach_key, finderUser)
	else:
		print 'User is in the cache'

	# get item from shard
	# item_cache_key = 'qr_items_' + str(user.id)
	# items = cache.get(item_cache_key)
	# if items is None:
	# 	item_query = Item.objects
	# 	set_user_for_sharding(item_query, user.id)
	# 	items = item_query.filter(owner=finderUser)

	# 	cache.set(item_cache_key, [item.item_id for item in items]) # store the item_id's so that we can get each from the cache
	# else:
	# 	item_vals = list()
	# 	still_need = list()
	# 	print 'Items are in cache'
	# 	cache = get_cache('items')
	# 	for item_id in items:
	# 		single_item_cache_key = 'qr_item_' + str(item_id) # have single item cache as well so that
	# 		cached_item = cache.get(single_item_cache_key)
	# 		if cached_item:
	# 			item_vals.append(cached_item)
	# 		else:
	# 			still_need.append(long(item_id))

	# 	if len(still_need) > 0:
	# 		item_query = Item.objects
	# 		set_user_for_sharding(item_query, user.id)
	# 		items = item_query.filter(owner=finderUser, item_id__in=still_need)
	# 		for item in items:
	# 			item_vals.append(item)
	item_query = Item.objects
	set_user_for_sharding(item_query, user.id)
	items = item_query.filter(owner=finderUser)

	context = {
		'user': finderUser,
		'items': items,
	}
	return render(request, 'my_qrcode/profile.html', context)

def item(request, user_id, item_id):
	'''List of recent posts by people I follow'''

	cache = caches['users']
	user_cach_key = 'qr_user_' + str(user_id)
	finderUser = cache.get(user_cach_key)
	if finderUser is None:
		try:
			# query user
			user_query = FinderUser.objects
			set_user_for_sharding(user_query, user_id)
			user = user_query.get(user_id=user_id)
			cache.set(user_cach_key, user)
		except FinderUser.DoesNotExist:
			return flashHomeMessage(request, 'Sorry, we could\'t find a user by that specification')
	else:
		user = finderUser
	# query items
	cache = caches['items']
	single_item_cache_key = 'qr_item_' + str(item_id) # have single item cache as well so that
	item = cache.get(single_item_cache_key)
	if item is None:
		try:
			item_query = Item.objects
			set_user_for_sharding(item_query, user_id)
			item = item_query.get(item_id=item_id)
			cache.set(single_item_cache_key, item)
		except Item.DoesNotExist:
			return flashHomeMessage(request, 'Sorry, we could\'t find an item by that specification')
	else:
		print 'Item is in cache'

	if item.is_public == False:
		if request.user.is_authenticated():
			set_user_for_sharding(user_query, user_id)
			logged_in_user = user_query.get(user_id=request.user.id)
			if item.owner != logged_in_user:
				return flashHomeMessage(request, 'This is not your item so you unfortunately can\'t view it')
		else:
			return flashHomeMessage(request, 'Please log in to view this item')

	context = {
		'user': user,
		'item': item,
	}
	return render(request, 'my_qrcode/item.html', context)

@login_required
def add_item(request):
	user_query = FinderUser.objects
	set_user_for_sharding(user_query, request.user.id)
	user = user_query.get(user_id=request.user.id)

	if request.method == 'POST':
		form = ItemForm(request.POST)

		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.owner = user
			new_item.status = Item.ITEM_NOT_LOST

			# set item id
			item_id = generate_item_id(user.user_id)

			while len(Item.objects.filter(item_id=item_id)):
				item_id = generate_item_id(user.user_id)

			new_item.item_id = item_id

			new_item.save()

			# add it to the cache
			# cache = caches['items']
			# single_item_cache_key = 'qr_item_' + str(item_id) # have single item cache as well so that
			# cache.set(single_item_cache_key, new_item)

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
	# get user from shard
	user_query = FinderUser.objects
	set_user_for_sharding(user_query, request.user.id)
	user = user_query.get(user_id=request.user.id)
	# get item from shard
	#item = get_object_or_404(Item, item_id=item_id)
	item_query = Item.objects
	set_user_for_sharding(item_query, request.user.id)
	item = item_query.get(item_id=item_id)

	if item.owner != user:
		return flashHomeMessage(request, 'This isn\'t your item')

	if request.method == 'POST':
		form = ItemForm(request.POST, instance=item)

		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.save()
			# add it to the cache
			# cache = caches['items']
			# single_item_cache_key = 'qr_item_' + str(item_id) # have single item cache as well so that
			# cache.set(single_item_cache_key, new_item)
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
	# get user from shard
	user_query = FinderUser.objects
	set_user_for_sharding(user_query, request.user.id)
	user = user_query.get(user_id=request.user.id)
	# get item from shard
	item_query = Item.objects
	set_user_for_sharding(item_query, request.user.id)
	item = item_query.get(item_id=item_id)

	if item.owner != user:
		return flashHomeMessage(request, 'This isn\'t your item')

	if request.method == 'POST':
		item.delete()
		# remove it from the cache
		cache = caches['items']
		single_item_cache_key = 'qr_item_' + str(item_id) # have single item cache as well so that
		cache.delete(single_item_cache_key)
		return HttpResponseRedirect(reverse('my_qrcode:profile', args=()))

	context = {
		'user': user,
		'item': item,
	}
	return render(request, 'my_qrcode/item_delete.html', context)

@login_required
def generate(request, item_id):
	# get user from shard
	user_query = FinderUser.objects
	set_user_for_sharding(user_query, request.user.id)
	user = user_query.get(user_id=request.user.id)
	# get item from shard
	item_query = Item.objects
	set_user_for_sharding(item_query, request.user.id)
	item = item_query.get(item_id=item_id)

	if item.owner != user:
		return flashHomeMessage(request, 'This isn\'t your item')

	# this is where we'll create the qrcode
	# make this the full site url, for now leave it as this dummy url
	qr_url = '/found/' + str(user.user_id) + '/' + str(item_id) + '/' 
	
	qr_uri = request.build_absolute_uri(qr_url) # the full absolute uri to be sent to the qrcode app

	# generate the qr_code
	img = qrcode.make(qr_uri)
	qr_filename = 'qr_' + str(item.item_id) + '.png'
	img.save(settings.MEDIA_ROOT + qr_filename)

	context = {
		'user': user,
		'item_id': item_id,
		'qr_url': qr_uri,
		'qr_image_source_url': settings.MEDIA_URL + qr_filename
	}
	return render(request, 'my_qrcode/generate.html', context)

def found(request, user_id, item_id):
	try:
		# get user from shard
		user_query = FinderUser.objects
		set_user_for_sharding(user_query, user_id)
		user = user_query.get(user_id=user_id)
		# get item from shard
		#item = get_object_or_404(Item, item_id=item_id)
		item_query = Item.objects
		set_user_for_sharding(item_query, user_id)
		item = item_query.get(item_id=item_id)
	except FinderUser.DoesNotExist:
		return flashHomeMessage(request, 'Sorry, we could\'t find a user by that specification')
	except Item.DoesNotExist:
		return flashHomeMessage(request, 'Sorry, we could\'t find an item by that specification')

	# mark the item as found here
	if item.status == Item.ITEM_LOST:
		item.status = Item.ITEM_FOUND
		item.save()

	context = {
		'user': user,
		'item': item,
	}
	return render(request, 'my_qrcode/found.html', context)
