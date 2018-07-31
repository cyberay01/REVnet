  var geocoder;
	var map;

	// setup initial map
	function initialize() {
		geocoder = new google.maps.Geocoder();							// create geocoder object
		var latlng = new google.maps.LatLng(40.6700, -73.9400);			// set default lat/long (new york city)
		var mapOptions = {												// options for map
			zoom: 8,
			center: latlng
		}
		map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);	// create new map in the map-canvas div
	}

	// function to geocode an address and plot it on a map
	function codeAddress(address) {
		geocoder.geocode( { 'address': address}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				map.setCenter(results[0].geometry.location);			// center the map on address
				var marker = new google.maps.Marker({					// place a marker on the map at the address
					map: map,
					position: results[0].geometry.location
				});
			} else {
				alert('Geocode was not successful for the following reason: ' + status);
			}
		});
	}

  google.maps.event.addDomListener(window, 'load', initialize);
