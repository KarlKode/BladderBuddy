$(document).ready(function() {
    var markers = {};
    var lastCenter = null;

    function loadMarkers() {
        var center = map.getCenter();
        var lat = center.lat();
        var lng = center.lng();

        if (lastCenter == null ||
            Math.abs(lastCenter.lat() - lat) > 0.0005 ||
            Math.abs(lastCenter.lng() - lng) > 0.001) {
            $.ajax({
                url: apiURLList,
                data: "lat=" + lat + "&lng=" + lng
            }).done(function(data) {
                    lastCenter = center;
                    var newMarkers = {};

                    $.each(data.toilets, function(_, toilet){
                        if (toilet.id in markers) {
                            newMarkers[toilet.id] = markers[toilet.id];
                            delete markers[toilet.id];
                        } else {
                            var marker = new google.maps.Marker({
                                position: new google.maps.LatLng(toilet.lat, toilet.lng),
                                map: map,
                                title: toilet.title
                            });
                            marker.toilet = toilet;
                            google.maps.event.addListener(marker, 'click', showToilet);
                            newMarkers[toilet.id] = marker;
                        }
                    });

                    $.each(markers, function(id, marker) {
                        marker.setMap(null);
                    });

                    markers = newMarkers;
                });
        }
    }

    var toiletInfoWindow = null;

    function closeToiletInfoWindow() {
        if (toiletInfoWindow != null) {
            toiletInfoWindow.close();
        }
    }

    function showToilet() {
        closeToiletInfoWindow();
        var marker = this;
        map.panTo(marker.getPosition());
        toiletInfoWindow = new google.maps.InfoWindow({
            content: 'Toilet ' + marker.toilet.title
        });
        toiletInfoWindow.open(map, marker);
    }

    var mapOptions = {
        disableDefaultUI: true,
        center: new google.maps.LatLng(47.375312, 8.532493),
        zoom: 16,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

    google.maps.event.addListener(map, 'center_changed', function() {
        loadMarkers();
    });

    loadMarkers();

    var addMarker = null;
    var addInfoWindow = null;

    function removeMarker() {
        if (addMarker != null) {
            addMarker.setMap(null);
        }
        if (addInfoWindow != null) {
            $("body").append(addInfoWindow.getContent());
            $("#addInfoWindow").hide();
            addInfoWindow.close();
        }
    }

    $('#addButton').on('click', function() {
        removeMarker();

        addMarker = new google.maps.Marker({
            position: map.getCenter(),
            map: map,
            title: 'Add a new toilet',
            draggable: true,
            animation: google.maps.Animation.DROP
        });

        var addInfoWindowContent = $("#addInfoWindow");
        addInfoWindow = new google.maps.InfoWindow({
            content: addInfoWindowContent.get(0)
        });
        addInfoWindowContent.show();
        addInfoWindow.open(map, addMarker);

        google.maps.event.addListener(addInfoWindow, 'closeclick', function() {
            removeMarker();
        })
    });

    $('#addAddressLookupButton').on('click', function() {
        var geo = new google.maps.Geocoder();
        geo.geocode({
            address: $('#addAddressLookup').val()
        },
        function(result, status) {
            if (result.length > 0) {
                var latlng = result[0].geometry.location;
                addMarker.setPosition(latlng);
                map.panTo(latlng);
            }
        });
    });

    $('#addToiletButton').on('click', function() {
        $('#addModal').modal();
    });

    $('#addTimeOpen').timepicker({
        defaultTime: false,
        showMeridian: false
    });

    $('#addTimeClose').timepicker({
        defaultTime: false,
        showMeridian: false
    });

    $('#addSubmit').on('click', function() {
        $.ajax({
            type: "PUT",
            url: apiURLAdd,
            data: {
                'title': $('#addTitle').val(),
                'description': $('#addDescription').val(),
                'time_open': $('#addTimeOpen').val(),
                'time_close': $('#addTimeClose').val(),
                'lat': addMarker.getPosition().lat(),
                'lng': addMarker.getPosition().lng()
            },
            success: function(data, textStatus, jqXHR) {
                console.log(data);
            }
        });
    });
});
