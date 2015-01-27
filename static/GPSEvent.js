console.log("is this working?");

var map;
var geocoder;
var marker;
var currentLoc;
var distanceDiv;

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
	return new google.maps.LatLng(36.112666, -115.176293);
    };

    var hellYeah = function(position) {
	map = document.getElementById('map-test');
        mappy = new google.maps.Map(map, mapOptions);

        latitude = position.coords.latitude;
        longitude = position.coords.longitude;
	var locationArray = [latitude, longitude];
        var location = new google.maps.LatLng(latitude, longitude);
        console.log(location)
        currentLoc = location
        console.log(currentLoc)
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
        return location
    };

    var geographicCoord = navigator.geolocation.getCurrentPosition( hellYeah, ahNo);
    console.log('locating complete.');
    console.log("button action complete");

}


var distTest = function() {
    distance = distanceFunc(currentLoc, new google.maps.LatLng(25.7877, -80.2241), 'dist-test')
}

var distanceFunc = function (origin, destination, div){
    console.log("in distanceFunc");
    var service = new google.maps.DistanceMatrixService();
    //var origin = location;
    distanceDiv = div;
    console.log(origin);
    console.log(destination);
    service.getDistanceMatrix(
	{
	    origins: [origin],
	    destinations: [destination],
            travelMode: google.maps.TravelMode.WALKING,
	    unitSystem: google.maps.UnitSystem.IMPERIAL,
            avoidHighways: false,
            avoidTolls: false
	}, callback);
}


function callback (response, status) {
    console.log("in callback")
    if (status != google.maps.DistanceMatrixStatus.OK){
        alert("Error with Distance:" + status);
    } else {
        console.log(response);
	var origins = response.originAddresses;
        console.log(origins);
	var destinations = response.destinationAddresses;
        console.log(destinations);
        var output = document.getElementById(distanceDiv);
        output.InnerHTML = '';
  	for (var i = 0; i < origins.length; i++){
  	    var results = response.rows[i].elements;
  	    for (var j = 0; j < results.length; j++){
                output.innerHTML = "";
		output.innerHTML += results[j].distance.text + ", which would take " + results[j].duration.text + " to complete.<br>";
            }
        }
    }
}

window.addEventListener("load", function getGeoLoc() {
  action()
  var storage = document.getElementById('loc')
  if (storage != null){
    storage.value = currentLoc;
  }
    //console.log(storage);
    action();
}, false);

/*
  DEAD CODE (Could be used in future for storing distance variables) CAN IGNORE
  var element = results[j];
  var dist = element.distance.text;
  console.log (dist)
  var dura = element.duration.text;
  var from = origins[i];
  var to = origins[i];
  answer[0] = dist;
  }
  }

  return answer;
  } else {
  alert("Distance Calculation failed due to: " + status);
  return answer;
  }
  }
  } */
