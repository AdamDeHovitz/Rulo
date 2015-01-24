console.log("is this working?");

var map;
var geocoder;
var marker;

var action = function () {
    console.log("button action begun");
    geocoder = new google.maps.Geocoder();
    var address;

    var mapOptions = {
	     zoom: 14
    };

    map = document.getElementById('map-test');

    if (!navigator.geolocation){
       map.innerHTML = "Geolocation is not supported by this browser. Please update to experience our awesomeness.";
       return;
    }


    var ahShit = function() {
      map.innerHTML = "We were unable to retrieve your location, our apologies.";
	console.log("ah noes,its an error");
      return new google.maps.LatLng(51.208317, 3.224883);
    };


    var hellYeah = function(position) {
        map = new google.maps.Map(map, mapOptions);

        latitude = position.coords.latitude;
        longitude = position.coords.longitude;
	var locationArray = [latitude, longitude];

        var location = new google.maps.LatLng(latitude, longitude);
        map.setCenter(location);
        console.log('map function finished. Latitude is: ' + latitude + " Longitude is: " + longitude);
	console.log(location);
	geocoder.geocode({'latLng': location}, function(results, status){
	    if (status == google.maps.GeocoderStatus.OK){
		if (results[0]) {
              marker = new google.maps.Marker({
		position: geographicCoord,
		map: map
              });
		    console.log('assign address');
		    address = results[0].formatted_address;
		    console.log(results[0].formatted_address);
		    var wordPlace = document.getElementById('map-location');
		    console.log(address);
		    wordPlace.innerHTML = address;
		}
	    } else {
		alert("Geocoder failed due to: " + status);
		address = "An error has arisen with the location identification.";
	    }
	});

	console.log('address actions completed');
        return locationArray
    };

    var geographicCoord = navigator.geolocation.getCurrentPosition( hellYeah, ahShit);
    console.log('locating complete.');
    console.log("button action complete");
}

var disctance = function (origin, destination){
    var service = google.maps.DistanceMatrixService();

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
	    }
	    else {
	       alert("Distance Calculation failed due to: " + status);
         return distance;
	    }
    }
    return distance;
}

/*var showPosition = function(position) {
    var lat = document.getElementById("lat");
    var long = document.getElementById("long");

    lat.value = position.coords.latitude;
    console.log(lat.value + "Hellooooo");
    long.value = position.coords.longitude;
    console.log(long.value + "heyyyyyyyyy");}

    function getLocation() {
    if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
    }
    }
var x = showPosition(position)
x()*/
