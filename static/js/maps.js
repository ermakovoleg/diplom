var myMap;
var myGeoObject;

ymaps.ready(init);

function init (){
    ymaps.geolocation.get().then(function(res){
            mySMap = new ymaps.Map('map',{
            zoom:14,
            center: res.geoObjects.get(0).geometry.getCoordinates(),
            type:'yandex#hybrid',
            controls: ['zoomControl', 'typeSelector',  'fullscreenControl']});
    });
}

    function openmap(type,obj){
        if (myGeoObject){
            myGeoObject.geometry.getCoordinates =null;
            myMap.geoObjects.remove(myGeoObject);
        }
        switch (type){
            case 'P':
                myGeoObject = new ymaps.Placemark([]);
                if (obj.value!=""){myGeoObject = new ymaps.Placemark(eval(obj.value));}
            break

            case 'L':
                myGeoObject = new ymaps.Polyline([]);
                if (obj.value!=""){ myGeoObject = new ymaps.Polyline(eval(obj.value));}
            break

            case 'Z':
                myGeoObject = new ymaps.Polygon([]);
                if (obj.value!=""){myGeoObject = new ymaps.Polygon(eval(obj.value));}
            break
}


        myMap.geoObjects.add(myGeoObject);
        myGeoObject.editor.startDrawing();
        document.getElementById('save').onclick = function () {
            obj.value=stringify(myGeoObject.geometry.getCoordinates())  ;
            myMap.geoObjects.remove(myGeoObject);
         };
    }

function stringify (coords) {
    var res = '';
    if ($.isArray(coords)) {
        res = '[ ';
        for (var i = 0, l = coords.length; i < l; i++) {
            if (i > 0) {
                res += ', ';
            }
            res += stringify(coords[i]);
        }
        res += ' ]';
    } else if (typeof coords == 'number') {
        res = coords.toPrecision(6);
    } else if (coords.toString) {
        res = coords.toString();
    }

    return res;
}