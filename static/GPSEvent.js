console.log("is this working?");

var map;
var mappy;
var geocoder;
var marker;
var myAddress;
var bounds = new google.maps.LatLngBounds();
var markersArray = [];

var action = function () {
    console.log("button action begun");
    geocoder = new google.maps.Geocoder();
    var address;

    var mapOptions = {
	center: new google.maps.LatLng(0,0),
	zoom: 14,
	mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = document.getElementById('map-test');

    if (!navigator.geolocation){
       map.innerHTML = "Geolocation is not supported by this browser. Please update to experience our awesomeness.";
       return;
    }


    var ahNo = function() {
      map.innerHTML = "We were unable to retrieve your location, our apologies.";
	console.log("ah noes,its an error");
	return new google.maps.LatLng(51.208317, 3.224883);
    };
    
    var hellYeah = function(position) {
	map = document.getElementById('map-test');
        mappy = new google.maps.Map(map, mapOptions);
	
        latitude = position.coords.latitude;
        longitude = position.coords.longitude;
	var locationArray = [latitude, longitude];
        var location = new google.maps.LatLng(latitude, longitude);
        mappy.setCenter(location);
        //console.log('map function finished. Latitude is: ' + latitude + " Longitude is: " + longitude);
	      //console.log(location);
	geocoder.geocode({'latLng': location}, function(results, status){
	    if (status == google.maps.GeocoderStatus.OK){
		if (results[0]) {
		    var marker = new google.maps.Marker({
			position: geographicCoord,
			title: "this is a marker",
			map: mappy
		    }); 
		    address = results[0].formatted_address;
		    myAddress = address;
		    var wordPlace = document.getElementById('map-location');
		    //console.log(address);
		    wordPlace.innerHTML = address;
		    map.innerHTML = mappy;
		    console.log(mappy);
		}
	    } else {
		alert("Geocoder failed due to: " + status);
		address = "An error has arisen with the location identification.";
	    }
	});

	//console.log('address actions completed');
        return locationArray
    };

    var geographicCoord = navigator.geolocation.getCurrentPosition( hellYeah, ahNo);
    //console.log('locating complete.');
    //console.log("button action complete");
}

var origin = myAddress;
var destination = myAddress; // need to get the event's location

var destinationIcon = 'https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=D|FF0000|000000';
var originIcon = 'https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=O|FFFF00|000000';

function initialize() {
    var opts = {
	center: new google.maps.LatLng(55.53, 9.4),
	zoom: 10
    };
    map = new google.maps.Map(document.getElementById('map-test'), opts);
    geocoder = new google.maps.Geocoder();
}

function thisFunc() {
    var service = new google.maps.DistanceMatrixService();
    service.getDistanceMatrix(
	{
	    origins: [origin],
	    destinations: [destination],
	    travelMode: google.maps.TravelMode.WALKING,
	    unitSystem: google.maps.UnitSystem.METRIC,
	    avoidHighways: false,
	    avoidTolls: false
	}, callback);
}

function callback(response, status) {
    if (status != google.maps.DistanceMatrixStatus.OK) {
	alert('Error was: ' + status);
    } else {
	var origins = origin;
	var destinations = destination;
	var outputDiv = document.getElementById('map-test');
	outputDiv.innerHTML = '';
	deleteOverlays();
	
	for (var i = 0; i < origins.length; i++) {
	    var results = response.rows[i].elements;
	    addMarker(origins[i], false);
	    for (var j = 0; j < results.length; j++) {
		addMarker(destinations[j], true);
		outputDiv.innerHTML += origins[i] + ' to ' + destinations[j]
		    + ': ' + results[j].distance.text + ' in '
		    + results[j].duration.text + '<br>';
	    }
	} 
    }
}

function distanceFunc(){
    google.maps.event.addDomListener(window, "load", thisFunc());
}

function addMarker(location, isDestination) {
    var icon;
    if (isDestination) {
      icon = destinationIcon;
  } else {
      icon = originIcon;
  }
    geocoder.geocode({'address': location}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
	bounds.extend(results[0].geometry.location);
	map.fitBounds(bounds);
	var marker = new google.maps.Marker({
          map: mappy,
          position: results[0].geometry.location,
          icon: icon
      });
	markersArray.push(marker);
    } else {
	alert('Geocode was not successful for the following reason: '
            + status);
    }
  });
}

function deleteOverlays() {
    for (var i = 0; i < markersArray.length; i++) {
      markersArray[i].setMap(null);
  }
    markersArray = [];
}


/* var distanceFunc = function (origin, destination){
    console.log("in distanceFunc");
    var service = google.maps.DistanceMatrixService();
    //var origin = location;
    console.log(origin);
    console.log(service.getDistanceMatrix);
    var distance = service.getDistanceMatrix(
	{
	    origins: origin,
	    destinations: destination,
	    travelMode: google.maps.TravelMode.WALKING,
	    unitSystem: google.maps.UnitSystem.IMPERIAL
	}, callback);
    
    function callback (response, status) {
	var distance = [];
	if (status == google.maps.GeocoderStatus.OK){
	    var origins = response.originAddress;
	    var destinations = response.destinationAddresses;
	    for (var i = 0; i < origins.length; i++){
		var results = response.rows[i].elements;
		for (var j = 0; j < results.length; j++){
		    var element = results[j];
		    var dist = element.distance.text;
		    var dura = element.duration.text;
		    var from = origins[i];
		    var to = origins[i];
		    distance[(i*results.length) + j] = dist;
		}
	    }
	    return distance;
	} else {
	    alert("Distance Calculation failed due to: " + status);
	    return distance;
	}
    }
    return distance[0];
} */
