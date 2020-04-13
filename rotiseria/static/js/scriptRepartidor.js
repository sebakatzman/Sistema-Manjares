//Iniciamos el mapa con los marcadores del JSON
var panorama;
var pedidoActivo;
var pedidoAnterior;

function initMap(){
  var ushuaia = {lat:-54.8161769 ,lng: -68.3278668};
  var map = new google.maps.Map(document.getElementById('map'),{
    zoom: 13,
    center: ushuaia,
    streetViewControl: false,
  });

  //agrego letras a los marcadores
  var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var labelIndex = 0;

  //ARREGLO DE MARCADORES
  var markers = [];

  var informacion = new google.maps.InfoWindow();
  if (!(markersData.length == 1)) {
    for (var i=0; i<markersData.length; i++){
      if (i == 0) {
        pedidoAnterior = markersData[i];
      }
      var punto = {lat:markersData[i].lat ,lng: markersData[i].long};
  
      var marker = new google.maps.Marker({
        position: punto,
        label: labels[labelIndex++ % labels.length],
        map: map,
        data: markersData[i]
      });
      direccion = markersData[i].dir == 'General Manuel Belgrano 43'
      if (direccion) {
        marker.addListener('click', function(){
          var content = '<h4>' + this.data.dir + '</h4>' +
            '<h6>' + this.data.nombre + '</h6>';
            informacion.setContent(content);
            informacion.open(map, this);
        });
      } else {
        //si estado = entregado, entonces mostrar informacion entregada
        if ((i == 0) && !(direccion)) {
          marker.addListener('click', function(){
            var content = '<h4>' + this.data.dir + '</h4>' +
              '<h6>Pedido N° ' + this.data.id + '</h6>' +
              '<h6>¡ENTREGADO!</h6>';
              informacion.setContent(content);
              informacion.open(map, this);
          });
        } else {
          //sino el estado esta como enviado, entonces agregar informacion completa
          marker.addListener('click', function(){
            pedidoActivo = this.data;
            var content = '<h4>' + this.data.dir + '</h4>' +
              '<h6>Pedido N° ' + this.data.id + '</h6>' +
              '<button type="button" class="btn btn-success" id="abrir" onclick="mostrar()">Detalles</button>' +
              '<input id="latitud" type="hidden" size="50" value="'+ this.data.lat +'"/>' +
              '<input id="longitud" type="hidden" size="50" value="'+ this.data.long +'"/>';
              informacion.setContent(content);
              informacion.open(map, this);
          });
        }
      }
      markers.push(marker);
    }

    //streetView
    panorama = map.getStreetView();
    panorama.setPov(/** @type {google.maps.StreetViewPov} */({
      heading: 265,
      pitch: 0
    }));
    

    //TRAZANDO EL CAMINO ENTRE EL MARCADOR INICIO -- (marcadores de por medio) -- FIN
    var objConfigDR = {
      map: map,
      suppressMarkers: true,
      sensor: false
    }

    var waypoints = [];
    for (var index = 0; index < markers.length; index++) {
      waypoints.push({location: markers[index].position, stopover: false});
    };
      
    var objConfigDS = {
      origin: markers[0].position, //Lat o Long - String
      destination: markers[markers.length-1].position,
      waypoints: waypoints,
      travelMode: google.maps.TravelMode.DRIVING
    }

    var ds = new google.maps.DirectionsService(); //obtiene las coordenadas
    var dr = new google.maps.DirectionsRenderer(objConfigDR); //traduce coordenadas a la ruta visible

    ds.route(objConfigDS, fnRutear);
    function fnRutear(resultados, status) {
        if (status == 'OK'){
            dr.setDirections(resultados);
        } else {
            alert('Error: ' + status);
        }
    }
  }
  
}

function street() {
  ocultar();
  var toggle = window.panorama.getVisible();
  if (toggle == false) {
    var latitud = parseFloat(document.getElementById('latitud').value);
    var longitud = parseFloat(document.getElementById('longitud').value);
    window.panorama.setVisible(true);
    window.panorama.setPosition({lat: latitud, lng: longitud});
  } else {
    window.panorama.setVisible(false);
  }
}