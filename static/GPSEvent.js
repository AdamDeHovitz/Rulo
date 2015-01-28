console.log("is this working?");

var map;
var geocoder;
var marker;
var currentLoc;
var distanceDiv;
var start;


var waitUp = true;

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
       alert("Geolocation is not supported by this browser. Please update to experience our awesomeness.");
       return;
    }


    var ahNo = function() {
	alert("We were unable to retrieve your location, our apologies.");
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
        currentLoc = location;
        storage = document.getElementById('loc');
        place =document.getElementById('yourLocation');
        if (storage != null){
           console.log("still working?");
           storage.value = currentLoc;
           console.log("This is storage:");
           console.log(storage.value);
        }
        if (place != null){
           console.log("still working?");
           place.value = currentLoc;
           console.log("This is storage:");
           console.log(place.value);
           waitUp = false;
        }
        console.log(currentLoc);

        //Distance
        if (start != null){
          console.log(start);
          //yes this is the wrong way to do it,
          var realStart =  start.substr(1, start.length -2);
          realStart = realStart.split(',');
          console.log(realStart);
          var destination = new google.maps.LatLng(parseFloat(realStart[0]), parseFloat(realStart[1]));
          console.log("Destination Object:");
          console.log(destination);
          var origin = currentLoc;
          console.log("originObject:");
          console.log(origin);
          distanceFunc (origin, destination, 'dist');
        }


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
		    var wordPlace = document.getElementById('address');
		    var mapi = document.getElementById('map-test');
		    console.log(address);
        if (wordPlace != null){
		        wordPlace.value = address;
            console.log("Testing WordPlace:");
            console.log(wordPlace.value);
        }
		    //map.innerHTML = new google.maps.LatLng(latitude,longitude);
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
    distance = distanceFunc(currentLoc, document.getElementById(), 'dist')
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
  	for (var i = 0; i < origins.length; i++){
  	    var results = response.rows[i].elements;
  	    for (var j = 0; j < results.length; j++){
		        output.innerHTML += results[j].distance.text + ", which is " + results[j].duration.text + " by Driving.";
            //console.log(output.value);
            }
        }
    }
}


window.addEventListener("load", function getGeoLoc() {
    start = document.getElementById("dist").innerHTML;
    document.getElementById("dist").innerHTML = "";
    document.getElementById("dist").style.visibility="visible";
    action();

    var NOTstart = document.getElementById("latLong").value;
    /*if (start != null){
      console.log(start);
      //yes this is the wrong way to do it,
      var realStart =  start.substr(1, start.length -2);
      realStart = realStart.split(',');
      console.log(realStart);
      var destination = new google.maps.LatLng(parseFloat(realStart[0]), parseFloat(realStart[1]));
      console.log("Destination Object:");
      console.log(destination);
      var origin = currentLoc;
      console.log("originObject:");
      console.log(origin);
      distanceFunc (origin, destination, 'dist');
    }*/
    //distTest();
    //console.log(storage);
    //action();
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
