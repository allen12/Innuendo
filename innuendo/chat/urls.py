from django.conf.urls import url

from . import views

app_name = "chat"
urlpatterns = [
	url(r"^$", views.index, name = "index"),
	url(r"^(?P<message_id>[0-9]+)/$", views.detail, name = "detail"),
	url(r"^(?i)submitmessage/$", views.submitmessage, name = "submitmessage"),
	url(r"^(?i)submitmessage_aux/$", views.submitmessage_aux, name = "submitmessage_aux"),
]