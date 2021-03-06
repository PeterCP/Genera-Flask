var $map, $marker, $geocoder,
    $input = $('#map-search-input')[0],
    defaultLocation = {
        lat: 21.110959,
        lng: -89.61479
    };

function setPlace(location, label) {
    $('#map-latitude-input').val(location.lat());
    $('#map-longitude-input').val(location.lng());
    // if (label && label !== '') { // Unnecessary to check for empty.
    if (label) {
        $('#map-search-input').val(label);
    } else {
        $geocoder.geocode({location: location}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK && results.length > 0)
                $('#map-search-input').val(results[0].formatted_address);
            else
                console.error('Could not geocode address. Server ' +
                    'responded with satus: ' + status);
        });
    }
}

function initMap() {
    $map = new google.maps.Map($('#location-map')[0], {
        center: defaultLocation,
        zoom: 13
    });

    $geocoder = new google.maps.Geocoder;

    var autocomplete = new google.maps.places.Autocomplete($input);
    autocomplete.bindTo('bounds', $map);

    var infowindow = new google.maps.InfoWindow();
    $marker = new google.maps.Marker({
        map: $map,
        anchorPoint: new google.maps.Point(0, -29)
    });
    $marker.setPosition(defaultLocation);

    autocomplete.addListener('place_changed', function() {
        infowindow.close();
        $marker.setVisible(false);
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            window.alert("Autocomplete's returned place contains no geometry");
            return;
        }

        // If the place has a geometry, then present it on a map.
        if (place.geometry.viewport) {
            $map.fitBounds(place.geometry.viewport);
        } else {
            $map.setCenter(place.geometry.location);
            $map.setZoom(17);  // Why 17? Because it looks good.
        }
        $marker.setIcon({
            url: place.icon,
            size: new google.maps.Size(71, 71),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(17, 34),
            scaledSize: new google.maps.Size(35, 35)
        });
        $marker.setPosition(place.geometry.location);
        $marker.setVisible(true);

        var address = '';
        if (place.address_components) {
            address = [
                (place.address_components[0] && place.address_components[0].short_name || ''),
                (place.address_components[1] && place.address_components[1].short_name || ''),
                (place.address_components[2] && place.address_components[2].short_name || '')
            ].join(' ');
        }

        infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
        infowindow.open($map, $marker);
        console.log(address)
        // setPlace(place.geometry.location, address);
    });
}
