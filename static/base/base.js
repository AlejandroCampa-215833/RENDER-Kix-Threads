// Script para manejar el menú móvil
document.addEventListener('DOMContentLoaded', function() {
    // Función para cerrar el menú al hacer clic fuera
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navbarToggler = document.querySelector('.navbar-toggler');
    
    // Cerrar menú al hacer clic en un enlace
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link, .dropdown-item');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    });
    
    // Mejorar comportamiento de dropdowns en móvil
    if (window.innerWidth < 992) {
        const dropdownToggles = document.querySelectorAll('.nav-link[data-bs-toggle="dropdown"]');
        dropdownToggles.forEach(function(toggle) {
            toggle.addEventListener('click', function(e) {
                // Permitir que Bootstrap maneje el dropdown
            });
        });
    }
});

