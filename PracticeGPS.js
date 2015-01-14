var marker;
var defaultMarker = {
    animation: google.maps.Animation.DROP,
    draggable: true
}

var currentLocation={};
var map;


function initialize() {
    var mapOptions = {
	center: new google.maps.LatLng(
	    40.724531899999995,
		-73.7971586),
	zoom: 16,
	mapTypeId: google.maps.MapTypeId.ROADMAP
    }

    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    currentLocation = loadLocation(setMarker(marker), function(error){	
	switch(error.code) {
	case error.PERMISSION_DENIED:
	    console.log("User denied permission.");
	    break;
	case error.POSITION_UNAVAILABLE:
	    console.log("Geolocation/GPS unavailable.");
	    break;
	case error.TIMEOUT:
	    console.log("Geolocation request timed out.");
	    break;
	case error.UNKNOWN_ERROR:
	    console.log("Something wack happened.");
	    break;
    	}
    });

}
google.maps.event.addDomListener(window, 'load', initialize);





function setMarker(marker){
    /*
      var contentString = "<div class=\"align-center\"> <button class=\"align-center\" type=\"button\">Drop a Crumb</button> </div>"
      var infowindow = new google.maps.InfoWindow({
      content: contentString
      });
    */

    return function(latlng){
	var pos = new google.maps.LatLng(latlng.latitude, latlng.longitude);
	marker = new google.maps.Marker({
	    map: map,
	    position: pos,
	    animation: defaultMarker.animation,
	    draggable: defaultMarker.draggable
	});
	map.panTo(marker.getPosition());
	
	google.maps.event.addListener(marker, 'clicked', function(){
	    console.log("hello there");
	    toggleBounce(marker);
	    //infowindow.open(map, marker);
	})
	google.maps.event.addListener(marker, 'dragend', function(){
   	    map.panTo(marker.getPosition());
   	});
    }
};
function toggleBounce(marker) {
    if (marker.getAnimation() != null) {
    	marker.setAnimation(null);
    } else {
    	marker.setAnimation(google.maps.Animation.BOUNCE);
    }
}






//Callbacks
function loadLocation (callback, error){
    latlng = currentLocation;

    function getLocation(pos){
	latlng["latitude"] = pos.coords.latitude;
	latlng["longitude"] = pos.coords.longitude;
	callback(latlng);
    }

    var load = function() {
	if (navigator.geolocation) {
	    console.log("Loading location now....");
	    navigator.geolocation.getCurrentPosition(getLocation, error);
	}
    }();

};
