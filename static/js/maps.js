var myMap;

ymaps.ready(init);

function init (){
    var geolocation = ymaps.geolocation, coords = [geolocation.latitude, geolocation.longitude];

    // Создание экземпляра карты и его привязка к контейнеру с
    // заданным id ("map").
    myMap = new ymaps.Map('map', {
        // При инициализации карты обязательно нужно указать
        // её центр и коэффициент масштабирования.
        center: coords,
        zoom:14,
        type:'yandex#hybrid'
    });

    myMap.controls
        // Кнопка изменения масштаба.
        .add('zoomControl', { left: 5, top: 5 })
        // Список типов карты
        .add('typeSelector')
        // Стандартный набор кнопок
        .add('mapTools', { left: 35, top: 5 });



// document.getElementById('del').onclick = function () {
        // Для уничтожения используется метод destroy.

//myMap.geoObjects.remove(myGeoObject);
// myGeoObject.geometry.getCoordinates =null;
// document.getElementById('geometry').textContent=myGeoObject.geometry.getCoordinates();

// };

}
var myGeoObject;

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