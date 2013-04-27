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
                data: "lat=" + lat + "&lng=" + lng,
                success: function(data) {
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
                },
                error: function(data, textStatus, jqXHR) {
                    $('body').prepend(
                        $('<div>').addClass('alert').addClass('alert-error').append('Error - could not get nearby facilities!')
                    );
                }
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
        var content = '<h3>' + marker.toilet.title + '</h3>';
        if (marker.toilet.time_open && marker.toilet.time_close) {
            content += '<small>' + marker.toilet.time_open + ' - ' + marker.toilet.time_close + '</small>';
        }
        content += '<ul>';
        $.each(marker.toilet.tags, function(_, tag) {
            content += '<li>' + tag.title + '</li>';
        });
        if (marker.toilet.address != undefined) {
            content += '<textarea disabled="disabled">' + marker.toilet.address + '</textarea>';
        }
        if (marker.toilet.category.id == 3) {
            content += '<p>' + marker.toilet.category.title + ' (' + marker.toilet.price + ')</p>';
        } else if (marker.toilet.category.id == 4) {
            content += '<p>' + marker.toilet.category.title + ' (' + marker.toilet.code + ')</p>';
        } else {
            content += '<p>' + marker.toilet.category.title + '</p>';
        }
        if (marker.toilet.category.description != undefined) {
            content += '<textarea disabled="disabled">' + marker.toilet.category.description + '</textarea>';
        }

        toiletInfoWindow = new google.maps.InfoWindow({
            content: content
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

    var geo = new google.maps.Geocoder();

    $('#addAddressLookupButton').on('click', function() {
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

    function checkCategory() {
        $('#addPriceContainer').hide();
        $('#addCodeContainer').hide();
        switch ($('#addCategory').val()) {
            case '3':
                $('#addPriceContainer').show();
                break;
            case '4':
                $('#addCodeContainer').show();
                break;
        }
    }

    function checkTimes() {
        if ($('#addTime').is(':checked')) {
            $('#addTimeOpen').prop('disabled', false);
            $('#addTimeClose').prop('disabled', false);
        } else {
            $('#addTimeOpen').prop('disabled', true);
            $('#addTimeClose').prop('disabled', true);
        }
    }

    $('#addToiletButton').on('click', function() {
        $('#addModal').modal();
        $('#addCategory').empty();
        $.each(categories, function(_, category) {
            $('#addCategory').append('<option value=' + category.id + '>' + category.title + "</option>");
        });
        checkCategory();
        checkTimes();
    });

    $('#addCategory').on('change', checkCategory);

    $('#addTime').on('change', checkTimes);

    $('#addTimeOpen').timepicker({
        defaultTime: false,
        showMeridian: false
    });

    $('#addTimeClose').timepicker({
        defaultTime: false,
        showMeridian: false
    });

    function addFormCleanup() {
        $('#addTitle').empty();
        $('#addDescription').empty();
        $('#addCode').empty();
        $('#addPrice').empty();
        $('#addTimeOpen').empty();
        $('#addTimeClose').empty();
    }

    $('#addSubmit').on('click', function() {
        geo.geocode({
            'location': addMarker.getPosition()
        },
        function(result, status) {
            var address = null;
            if (result.length > 0) {
                address = result[0].formatted_address
            }
            $.ajax({
                type: "PUT",
                url: apiURLAdd,
                data: {
                    'title': $('#addTitle').val(),
                    'description': $('#addDescription').val(),
                    'lat': addMarker.getPosition().lat(),
                    'lng': addMarker.getPosition().lng(),
                    'address': address,
                    'category': $('#addCategory').val(),
                    'price': $('#addPrice').val(),
                    'code': $('#addCode').val(),
                    'time_open': $('#addTimeOpen').val(),
                    'time_close': $('#addTimeClose').val()
                },
                success: function(data, textStatus, jqXHR) {
                    $("#addModal").modal('hide');
                    addFormCleanup();
                    removeMarker();
                    lastCenter = null;
                    loadMarkers();
                },
                error: function(data, textStatus, jqXHR) {
                    $("#addModal").modal('hide');
                    addFormCleanup();
                    alert("error");
                }
            });
        });
    });
});
