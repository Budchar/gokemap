    window.addEventListener("map:init", function (e) {
        function poke_icon(poke_num){
            return L.icon({
                iconUrl: m_i(poke_num),
                iconSize: [40, 40],
                iconAnchor: [0, 0],
                popupAnchor: [-3, -26],
            });
        }
        var gym_icon = L.icon({
            iconUrl: pgp,
            iconSize: [24,24],
            iconAnchor: [0, 0],
            popupAnchor:  [-3, -26],
        });
        function egg_icon(tier){
            return L.icon({
            iconUrl: e_i(tier),
            iconSize: [32, 32],
            iconAnchor: [0, 0],
            popupAnchor:  [-3, -26],
            });
        }

        var detail = e.detail;
        L.geoJson(collection, {
            pointToLayer: function(feature, latlng){
                switch (feature.properties.icon[0]) {
                    case "p":
                        myicon=poke_icon(feature.properties.icon[1]);
                        break;
                    case "r":
                        myicon=egg_icon(feature.properties.icon[1]);
                        break;
                    case 0:
                        myicon=gym_icon;
                        break;
                    default:
                        console.log(`This is ${feature.id} icon error!`);
                }
                return L.marker(latlng, {icon:myicon});
            },
        }).addTo(detail.map);
    }, false);