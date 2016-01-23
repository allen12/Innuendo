from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import loader
from django.core.urlresolvers import reverse


from datetime import datetime

from .models import Message, User

# Create your views here.
def index(request):
	latest_message_list = Message.objects.all()
	context = {
		"latest_message_list": latest_message_list,
	}

	return render(request, "chat/index.html", context)

def detail(request, message_id):
	try:
		message = Message.objects.get(pk = message_id)
	except Message.DoesNotExist:
		raise Http404("Message does not exist")

	return render(request, "chat/detail.html", {"message": message})

def submitmessage(request):
	return render(request, "chat/submitmessage.html", {"error message": None})

def submitmessage_aux(request):

	# if any fields are blank, then reload the page!
	results = [request.POST.get("firstname"), request.POST.get("lastname"), request.POST.get("message")]
	for i in results:
		if i is None or i == "":
			return submitmessage(request)


	us = User(first_name = request.POST.get("firstname"), last_name = request.POST.get("lastname"), color = "FF0000")

	# check whether user already exists in the database, if not then add it
	if User.objects.filter(first_name = results[0], last_name = results[1]).exists() == False:
		us.save()
	else:
		us = User.objects.all()[0]

	ms = Message(user = us, text = request.POST.get("message"), timestamp = datetime.now())

	ms.save()

	return index(request)