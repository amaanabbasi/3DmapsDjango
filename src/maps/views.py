from django.shortcuts import render
from mapbox import Directions
# Create your views here.

def default_maps(request):
	# TODO: move Token to settings.py file
	mapbox_access_token = 'Make a free account on mapbox to get a token and put it here.'

	service = Directions()
	
	# Authentication
	service.session.params['access_token'] = mapbox_access_token
	origin = {
		    'type': 'Feature',
		    'properties': {'name': 'Portland, OR'},
		    'geometry': {
		        'type': 'Point',
		        'coordinates': [-122.7282, 45.5801]}
		        }
	destination = {
		    'type': 'Feature',
		    'properties': {'name': 'Bend, OR'},
		    'geometry': {
		        'type': 'Point',
		        'coordinates': [-121.3153, 44.0582]}
		        }
	response = service.directions([origin, destination], 'mapbox.driving')
	print(response)	        
	return render(request, 'details.html', {'mapbox_access_token':mapbox_access_token})
	