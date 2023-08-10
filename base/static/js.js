$(document).ready(function() {
  $('.owl-carousel').owlCarousel({
    loop: true, // Reproducción en bucle
    margin: 10, // Espacio entre las imágenes
    autoplay: true, // Reproducción automática
    autoplayTimeout: 3000, // Tiempo entre imágenes (3 segundos)
    autoplayHoverPause: true, // Pausar al pasar el cursor por encima
    responsive: {
      0: {
        items: 1 // Mostrar solo una imagen en pantallas pequeñas
      },
      768: {
        items: 2 // Mostrar dos imágenes en pantallas medianas
      },
      992: {
        items: 3 // Mostrar tres imágenes en pantallas grandes
      }
    }
  });
});