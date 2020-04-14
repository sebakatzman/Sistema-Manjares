
function mostrar() {
  document.getElementById('contenedor').style.height = '300px';
  document.getElementById('abrir').style.display = 'none';
  document.getElementById('cerrar').style.display = 'inline';
  document.getElementById('imagenMapa').src = 'http://maps.googleapis.com/maps/api/streetview?size=160x205&location='+ document.getElementById('latitud').value +','+ document.getElementById('longitud').value +'&sensor=false&key=AIzaSyC5bJ7e24SdcnhOtbqPMfC30MrOlhLyMTI';
  document.getElementById('domicilio').innerHTML = '<b>Dirección: </b>'+ pedidoActivo.dir;
  document.getElementById('nombre').innerHTML = '<b>Nombre: </b>'+ pedidoActivo.nombre;
  document.getElementById('telefono').innerHTML = '<b>Teléfono: </b>'+ pedidoActivo.telefono;
  document.getElementById('precio').innerHTML = '<b>Total: </b>'+ pedidoActivo.precio;
  document.getElementById('pago').innerHTML = '<b>Forma de pago: </b>'+ pedidoActivo.formaPago;
  document.getElementById('entregado').href = '/entregar_pedido/' + pedidoAnterior.id;
}
function ocultar() {
  document.getElementById('contenedor').style.height = '0';
  document.getElementById('abrir').style.display = 'inline';
  document.getElementById('cerrar').style.display = 'none';
}