# How to Add Maps + 3D buildings to Django Web App

In this post we will build a simple app in Django and add an
interactive map like the one you see above.

I assume that you have beginner or intermediate knowledge of Python and Django, and a little knowledge of Html and javascript. Otherwise you might have hard time following the tutorial. 

However, I have included instructions, wherever I thought it was neccessary.

# Basic Requirements

We will use the following tools to build our App.

* Python 3
* A [Mapbox account](https://www.mapbox.com/) to interact with their [web API](https://www.restapitutorial.com/) using [JavaScript](https://dev.to/underdogio/python-for-javascript-developers) .

The code for this blog post is also available on [Github]().

# Installing Dependencies

First, create a folder, name it whatever you want. Now, create a virtual environment using the following command.

>`python -m venv djangomaps`

Activate the virtualenv

>`.\Scripts\activate` (Windows users)

or

>`source djangomaps/bin/activate` (mac users)

The command prompt will change after activating the virtualenv. **djangomaps** in parentheses will be added before the path.

Now, install [Django]() package using pip.
> `pip install django==2.0.5`

This will install Django into the environment (djangomaps). 
# Sign-up for Mapbox

Head to the [Mapbox](https://www.mapbox.com/). Click on "Get started". Sign up for a free account. Once you have signed in.
Click the "JS Web" option. Then, choose "Use the Mapbox CDN" to install Mapbox GL JS. Once you have done that you will be provided with a access token, like this one "pk.eyJ1IjoIcGVuh29veCIsImEiOiJjampHNshreDkwbGZ5M3BxbXZkdDQ0dGdpIn1.-36WPGfz6NY90m3trPkNyw". We will use this token later.

# Getting Started with Django

Now, run the following command to start a Django project named djmaps:

>`django-admin startproject djmaps`

This command will create the boilerplate code structure to get our project started.

This is how the file structure should look like:
* djmaps
    * djmaps
        * `__init__.py`
        * `settings.py`
        * `urls.py`
        * `wsgi.py`
    * `manage.py`


>`cd djmaps`

Create a django app.

>`python manage.py startapp maps`

Django will create a new directory named `maps` for the project. Alright, first thing that we do after creating a new app in Django is to add it to the `settings.py` file. Change directory to `djmaps` and open up the `settings.py` file, add `maps` into the `INSTALLED_APPS` section like below:

```python
INSTALLED_APPS = [ 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'maps',  // Here
]
```
Save and close settings.py file.
Next, from the same directory open urls.py file and add the following two lines (#3 and #5), So that URLs will check the `map` app for appropriate URL matching.

```python
from django.contrib import admin
from django.urls import path
from django.conf.urls import include // #3 

urlpatterns = [
    path('', include('maps.urls')), // #5
    path('admin/', admin.site.urls),
]

```
<!-- In line 5, When a user makes a request for a page on our webapp, Django controller takes over to look the corresponding view via the urls.py file and then return the HTML response or a 404 not found error, if not found. -->
Save and close urls.py

Next change into the `djmaps/maps` directory. Create a new file named `urls.py` to contain routes for the maps app. 
<!-- Basically, url(Conf) is a set of patterns that Django will try to match the requested URL to find the correct view. -->
Add the following lines into the urls.py file you just created.

```python
from django.conf.urls import url                                                                                                                              
from . import views

urlpatterns = [ 
    url(r'', views.default_map, name="default"),
]
```

Save and close the file, Now from the same directory open `views.py` file and add the following lines.

```python
from django.shortcuts import render

# Create your views here.
def default_map(request):
    mapbox_access_token = 'your token'
    return render(request, 'map.html', {mapbox_access_token:mapbox_access_token})

```
Put the token that was mentioned before in the place of "`your token`".

We haven't yet created a `map.html` file. Now,
Create a directory for the template files named `templates` and inside it, Create a new file called `map.html`.

By the time, your file structure should look something like this:
* djmaps
    * djmaps
        *  `__init__.py`
        * `settings.py`
        * `urls.py`
        * `wsgi.py`
    * maps
        * `views.py`
        * `urls.py`
        * templates
            * `map.html`
        * (__more__...)
    * `manage.py`

Once you have done that, add the following html code in the `map.html` file.

```HTML
<!DOCTYPE html>
<html>
<head>
	<title> My maps </title>
	<script src='https://api.mapbox.com/mapbox-gl-js/v0.46.0/mapbox-gl.js'></script>
	<link href='https://api.mapbox.com/mapbox-gl-js/v0.46.0/mapbox-gl.css' rel='stylesheet' />
</head>

<body>
	<h6> Mapbox maps in your apps</h6>

	<div id='map' style='width: 95%; height:850px;'></div>
	<script>
		mapboxgl.accessToken = "{{ mapbox_access_token }}"

		var map = new mapboxgl.Map({
		container: 'map',
		style: 'mapbox://styles/mapbox/streets-v10',
		center: [77.2423,28.5972], // location
		zoom: 17,
		bearing: 0,
		pitch:100
	
		});

		// fulscreen button 
		map.addControl(new mapboxgl.FullscreenControl());

		// display a blue marker
		var marker = new mapboxgl.Marker()
  			.setLngLat([77.2423,28.5972])
  			.addTo(map);

  		// Navigation marker at top-left corner
  		var nav = new mapboxgl.NavigationControl();
  			map.addControl(nav, 'top-left');


  		// The 'building' layer in the mapbox-streets vector source contains building-height
        // data from OpenStreetMap.
		map.on('load', function() {
		    // Insert the layer beneath any symbol layer.
		    var layers = map.getStyle().layers;

		    var labelLayerId;
		    for (var i = 0; i < layers.length; i++) {
		        if (layers[i].type === 'symbol' && layers[i].layout['text-field']) {
		            labelLayerId = layers[i].id;
		            break;
		        }
		    }

		    map.addLayer({
		        'id': '3d-buildings',
		        'source': 'composite',
		        'source-layer': 'building',
		        'filter': ['==', 'extrude', 'true'],
		        'type': 'fill-extrusion',
		        'minzoom': 15,
		        'paint': {
		            'fill-extrusion-color': '#aaa',

		            // use an 'interpolate' expression to add a smooth transition effect to the
		            // buildings as the user zooms in
		            'fill-extrusion-height': [
		                "interpolate", ["linear"], ["zoom"],
		                15, 0,
		                15.05, ["get", "height"]
		            ],
		            'fill-extrusion-base': [
		                "interpolate", ["linear"], ["zoom"],
		                15, 0,
		                15.05, ["get", "min_height"]
		            ],
		            'fill-extrusion-opacity': .6
		        }
		    }, labelLayerId);
		});
	
		
	</script>

</body>
</html>	

```

That's it, we are done with code and it's the time to run the app.
In the command prompt type in:
>`python manage.py runserver`

This will start a server at PORT 8000.
To access your app, open browser and go to the following url:

>`localhost:8000`



