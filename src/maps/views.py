from django.shortcuts import render
from mapbox import Directions
# Create your views here.

def default_maps(request):
	# TODO: move Token to settings.py file
	mapbox_access_token = 'Make a free account on mapbox to get a token and put it here.'
	
	return render(request, 'details.html', {'mapbox_access_token':mapbox_access_token})
	