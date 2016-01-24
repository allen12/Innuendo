from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import loader
from django.core.urlresolvers import reverse


from datetime import datetime

from .models import Message, User, Group

from django.contrib import auth
from django.contrib.auth.models import User as Account


def index(request):
	return render(request, "chat/index.html", None)

def chat(request):
	if not request.user.is_authenticated():
		return render(request, "chat/index.html", {"error_message": "Please login."})

	account = request.user

	latest_message_list = Message.objects.all().order_by("-id")[:15]
	context = {
		"latest_message_list": latest_message_list,
		"first_name": account.first_name,
		"last_name": account.last_name,
	}

	return render(request, "chat/chat.html", context)

def detail(request, message_id):
	try:
		message = Message.objects.get(pk = message_id)
	except Message.DoesNotExist:
		raise Http404("Message does not exist")

	return render(request, "chat/detail.html", {"message": message})

def submitmessage(request):
	if not request.user.is_authenticated():
		return render(request, "chat/index.html", {"error_message": "Please login."})

	account = request.user

	us = User(first_name = account.first_name, last_name = account.last_name, color = "FF0000")
	# check whether user already exists in the database, if not then add it
	if User.objects.filter(first_name = account.first_name, last_name = account.last_name).exists() == False:
		us.save()
	else:
		us = User.objects.filter(first_name = account.first_name, last_name = account.last_name)[0]

	ms = Message(user = us, text = request.POST.get("message"), timestamp = datetime.now())
	ms.save()

	return chat(request)

def login(request):
	username = request.POST.get("username")
	password = request.POST.get("password")

	user = auth.authenticate(username = username, password = password)

	if user is not None and user.is_active:
		auth.login(request, user)
		return HttpResponseRedirect("/chat/chat/")
	else:
		return render(request, "chat/index.html", {"error_message": "Invalid login! Try again."})

def register(request):
	username = request.POST.get("username")
	first_name = request.POST.get("first_name")
	last_name = request.POST.get("last_name")
	password = request.POST.get("password")
	passwordagain = request.POST.get("passwordagain")
	email = request.POST.get("email")

	if username == "" or password == "" or passwordagain == "" or email == "" or first_name == "" or last_name == "":
		return render(request, "chat/index.html", {"error_message": "One or more fields were left blank!"})
	if password != passwordagain:
		return render(request, "chat/index.html", {"error_message": "Passwords do not match!"})

	if Account.objects.filter(username = username).exists():
		return render(request, "chat/index.html", {"error_message": "Username already exists!"})

	user = Account.objects.create_user(username = username, password = password, email = email, first_name = first_name, last_name = last_name)
	user.save()
	return render(request, "chat/index.html", {"error_message": "Registered! You may now log in."})