document.addEventListener('DOMContentLoaded', function() {
    // Manejo del botón de alternar filtros en móvil
    const toggleFiltersBtn = document.getElementById('toggleFilters');
    const filtersColumn = document.getElementById('filtersColumn');
    
    if (toggleFiltersBtn && filtersColumn) {
        toggleFiltersBtn.addEventListener('click', function() {
            filtersColumn.classList.toggle('show-filters');
        });
    }
    
    // Manejo de los filtros
    const filterForms = document.querySelectorAll('.filter-form');
    filterForms.forEach(form => {
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                form.submit();
            });
        });
    });
    
    // Manejo del botón "Cargar más"
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const nextPageUrl = this.getAttribute('href');
            
            fetch(nextPageUrl)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newProducts = doc.querySelectorAll('.product-card');
                    const productsContainer = document.querySelector('.products-container');
                    
                    newProducts.forEach(product => {
                        productsContainer.appendChild(product.cloneNode(true));
                    });
                    
                    // Actualizar el botón con la siguiente página
                    const newNextPage = doc.getElementById('loadMoreBtn');
                    if (newNextPage) {
                        loadMoreBtn.setAttribute('href', newNextPage.getAttribute('href'));
                    } else {
                        loadMoreBtn.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Error al cargar más productos:', error);
                });
        });
    }
    
    // Agregar a favoritos
    const addToFavoriteBtns = document.querySelectorAll('.add-to-favorites-btn');
    addToFavoriteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');
            const url = this.getAttribute('href');
            
            fetch(url)
                .then(response => {
                    if (response.ok) {
                        // Mostrar notificación
                        const toast = new bootstrap.Toast(document.getElementById('addToFavoritesToast'));
                        toast.show();
                    }
                })
                .catch(error => {
                    console.error('Error al agregar a favoritos:', error);
                });
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM para filtros
    const toggleFiltersBtn = document.getElementById('toggleFilters');
    const closeFiltersBtn = document.getElementById('closeFilters');
    const filtersColumn = document.getElementById('filtersColumn');
    
    // Crear backdrop para cerrar al hacer clic fuera
    const backdrop = document.createElement('div');
    backdrop.className = 'filter-backdrop';
    document.body.appendChild(backdrop);
    
    // Función para mostrar filtros
    function showFilters() {
        filtersColumn.classList.add('show');
        backdrop.classList.add('show');
        document.body.style.overflow = 'hidden'; // Prevenir scroll
    }
    
    // Función para ocultar filtros
    function hideFilters() {
        filtersColumn.classList.remove('show');
        backdrop.classList.remove('show');
        document.body.style.overflow = ''; // Restaurar scroll
    }
    
    // Event listeners para filtros
    if (toggleFiltersBtn) {
        toggleFiltersBtn.addEventListener('click', function(e) {
            e.preventDefault(); // Prevenir comportamiento predeterminado
            showFilters();
        });
    }
    
    if (closeFiltersBtn) {
        closeFiltersBtn.addEventListener('click', function(e) {
            e.preventDefault(); // Prevenir comportamiento predeterminado
            hideFilters();
        });
    }
    
    // Cerrar al hacer clic en el backdrop
    backdrop.addEventListener('click', hideFilters);
    
    // Cerrar filtros al cambiar a vista desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 768) {
            hideFilters();
        }
    });
    
    // Manejo de los filtros - autosubmit al cambiar
    const filterForms = document.querySelectorAll('.filter-form');
    filterForms.forEach(form => {
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                form.submit();
            });
        });
    });
    
    // Manejo del botón "Cargar más"
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const nextPageUrl = this.getAttribute('href');
            
            fetch(nextPageUrl)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newProducts = doc.querySelectorAll('.product-card');
                    const productsContainer = document.querySelector('.products-container');
                    
                    newProducts.forEach(product => {
                        productsContainer.appendChild(product.cloneNode(true));
                    });
                    
                    // Actualizar el botón con la siguiente página
                    const newNextPage = doc.getElementById('loadMoreBtn');
                    if (newNextPage) {
                        loadMoreBtn.setAttribute('href', newNextPage.getAttribute('href'));
                    } else {
                        loadMoreBtn.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Error al cargar más productos:', error);
                });
        });
    }
    
    // Agregar a favoritos
    const addToFavoriteBtns = document.querySelectorAll('.add-to-favorites-btn');
    addToFavoriteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');
            const url = this.getAttribute('href');
            
            fetch(url)
                .then(response => {
                    if (response.ok) {
                        // Mostrar notificación
                        const toast = new bootstrap.Toast(document.getElementById('addToFavoritesToast'));
                        toast.show();
                    }
                })
                .catch(error => {
                    console.error('Error al agregar a favoritos:', error);
                });
        });
    });
});