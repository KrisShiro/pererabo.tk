ymaps.ready(init);

function init() {
    // map initialization
    var myMap = new ymaps.Map("map", {
        center: [59.939063, 30.315239],
        zoom: 11,
        controls: ['zoomControl', 'typeSelector', 'geolocationControl',]
    });


    // search bar initialization
    var searchBar = new ymaps.SuggestView('search');
    let searchBarObject = $("#search");

    function sf() {
        // Delete this if world search
        let spbBounds = ymaps.geocode('Санкт-Петербург', {
            results: 1
        }).then(function (res) {
            let bounds = res.geoObjects.get(0).properties.get('boundedBy');
            myMap.setBounds(bounds);
        }).then(function() {
            let value = searchBarObject.val();
            ymaps.geocode(value, {
                results: 1,
                boundedBy: myMap.getBounds(),
                strictBounds: true
            }).then(function (res) {
                let firstObject = res.geoObjects.get(0),
                    coords = firstObject.geometry.getCoordinates(),
                    bounds = firstObject.properties.get('boundedBy');
                myMap.setBounds(bounds, {
                    checkZoomRange: true
                });
            })
        });
    }

    $('#search_button').click(sf);
    searchBarObject.bind('enterKey', sf);
    searchBarObject.keyup(function(e) {
        if (e.keyCode === 13) {
            $(this).trigger("enterKey");
        }
    });

    // adding objects on map
    let clusterer = new ymaps.Clusterer({
        preset: 'islands#grayClusterIcons',
        groupByCoordinates: false,
        clusterDisableClickZoom: false
    });

    let placesReadyToAdd = [];

    for (let i = 0; i < places_data.length; i++) {
        let coords = [places_data[i]['coordinate_x'], places_data[i]['coordinate_y']];
        placesReadyToAdd[i] = new ymaps.Placemark(coords, {
            data: [
                {weight: ((places_data[i]['type_mask'] & 1) !== 0) * 25, color: '#dc3545'},
                {weight: ((places_data[i]['type_mask'] & 2) !== 0) * 25, color: '#007bff'},
                {weight: ((places_data[i]['type_mask'] & 4) !== 0) * 25, color: '#28a745'},
                {weight: ((places_data[i]['type_mask'] & 8) !== 0) * 25, color: '#ffc107'},
            ],
            balloonContentHeader: 'Пункт #' + places_data[i]['id'],
            balloonContent: '<strong>Адрес</strong>: ' + places_data[i]['address'],
            iconCaption: '',
            iconContent: ''
        }, {
            iconLayout: "default#pieChart",
            iconPieChartRadius: 15,
            iconPieChartCoreRadius: 0,
            hideIconOnBalloonOpen: false
        });
    }
    clusterer.add(placesReadyToAdd);
    myMap.geoObjects.add(clusterer);


    let showPlasticButton = $("#show_plastic_button");
    let showPaperButton = $("#show_paper_button");
    let showGlassButton = $("#show_glass_button");
    let showAccumButton = $("#show_accum_button");
    let buttons = [showPlasticButton, showPaperButton, showGlassButton, showAccumButton];

    function reloadMapObjects() {
        // myMap.geoObjects.removeAll();
        clusterer.removeAll();
        let neededMasks = [];
        for (let i = 0; i < buttons.length; i++) {
            if (buttons[i].hasClass('activated')) {
                neededMasks.push(1 << i);
            }
        }

        for (let i = 0; i < places_data.length; i++) {
            let add = false;
            for (let j = 0; j < neededMasks.length; j++) {
                if ((places_data[i]['type_mask'] & neededMasks[j]) !== 0) {
                    add = true;
                    break;
                }
            }
            if (add) {
                clusterer.add(placesReadyToAdd[i]);
            }
        }
    }

    showPlasticButton.click(function () {
        showPlasticButton.toggleClass("activated bg-danger text-light");
        reloadMapObjects();
    });

    showPaperButton.click(function () {
        showPaperButton.toggleClass("activated bg-primary text-light");
        reloadMapObjects();
    });


    showGlassButton.click(function () {
        showGlassButton.toggleClass("activated bg-success text-light");
        reloadMapObjects();
    });


    showAccumButton.click(function () {
        showAccumButton.toggleClass("activated bg-warning text-light");
        reloadMapObjects();
    });
}
