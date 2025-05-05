document.addEventListener('DOMContentLoaded', function() {
    // Función para mostrar las notificaciones
    function showToast(toastId) {
        var toastElement = document.getElementById(toastId);
        var toast = new bootstrap.Toast(toastElement, {
            delay: 3000
        });
        toast.show();
    }
    
    // Agregar evento para el botón de favoritos
    const addToFavoritesBtn = document.querySelector('.add-to-favorites-btn');
    if (addToFavoritesBtn) {
        addToFavoritesBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');
            const url = this.getAttribute('href');
            
            // Realizar la solicitud al servidor
            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.ok) {
                    // Mostrar notificación de éxito
                    showToast('addToFavoritesToast');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
    
    // Agregar evento para el botón de agregar a la bolsa
    const addToCartBtn = document.querySelector('.add-to-cart-btn');
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            
            // Realizar la solicitud al servidor
            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.ok) {
                    // Mostrar notificación de éxito
                    showToast('addToCartToast');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});