console.log("is this working?");

var map;
var geocoder;
var marker;
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
        console.log('map function finished. Latitude is: ' + latitude + " Longitude is: " + longitude);
	      console.log(location);
	geocoder.geocode({'latLng': location}, function(results, status){
	    if (status == google.maps.GeocoderStatus.OK){
		if (results[0]) {
		    var marker = new google.maps.Marker({
			position: geographicCoord,
			map: mappy
		    });
		    //console.log('assign address');
		    address = results[0].formatted_address;
		    var wordPlace = document.getElementById('map-location');
		    var mapi = document.getElementById('map-test');
		    console.log(address);
		    wordPlace.innerHTML = address;
		    map.innerHTML = new google.maps.LatLng(latitude,longitude);
		    console.log(mappy);
		}
	    } else {
		alert("Geocoder failed due to: " + status);
		address = "An error has arisen with the location identification.";
	    }
	});

	console.log('address actions completed');
        return locationArray
    };

    var geographicCoord = navigator.geolocation.getCurrentPosition( hellYeah, ahNo);
    console.log('locating complete.');
    console.log("button action complete");
}


var distanceFunc = function (origin, destination){
    console.log("in distanceFunc");
    var service = google.maps.DistanceMatrixService();
    //var origin = location;
    console.log(origin);
    var distance = service.getDistanceMatrix(
	{
	    origins: origin,
	    destinations: destination,
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
}
