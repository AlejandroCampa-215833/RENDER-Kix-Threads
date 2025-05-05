document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todos los botones de eliminar favoritos
    const removeFavoriteButtons = document.querySelectorAll('.remove-favorite');
    
    // Agregar evento de clic a cada botón
    removeFavoriteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const url = this.getAttribute('href');
            const productCard = this.closest('.col');
            
            // Realizar solicitud AJAX para eliminar el favorito
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (response.ok) {
                    // Animar la eliminación del producto
                    productCard.style.transition = 'opacity 0.3s ease';
                    productCard.style.opacity = '0';
                    
                    setTimeout(() => {
                        productCard.remove();
                        
                        // Verificar si no quedan más favoritos
                        const remainingFavorites = document.querySelectorAll('.product-card');
                        if (remainingFavorites.length === 0) {
                            location.reload(); // Recargar para mostrar el mensaje de "no favoritos"
                        }
                    }, 300);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
    
    // Función para obtener el token CSRF de las cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
