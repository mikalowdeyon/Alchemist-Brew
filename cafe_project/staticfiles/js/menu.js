// menu.js - Handles add-to-cart functionality for the menu page

document.addEventListener('DOMContentLoaded', function() {
    // Function to add item to cart
    function addToCart(itemId, itemName, itemPrice) {
        // Get existing cart from localStorage or initialize empty array
        let cart = JSON.parse(localStorage.getItem('cart')) || [];

        // Check if item already exists in cart
        const existingItem = cart.find(item => item.id === itemId);

        if (existingItem) {
            // Increment quantity if item exists
            existingItem.quantity += 1;
        } else {
            // Add new item to cart
            cart.push({
                id: itemId,
                name: itemName,
                price: parseFloat(itemPrice),
                quantity: 1
            });
        }

        // Save updated cart to localStorage
        localStorage.setItem('cart', JSON.stringify(cart));

        // Optional: Show feedback to user (e.g., alert or toast)
        alert(`${itemName} added to cart!`);

        // Optional: Update cart icon or badge if exists
        updateCartBadge();
    }

    // Function to update cart badge (if cart icon has a badge)
    function updateCartBadge() {
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);

        // Assuming there's a cart badge element, e.g., <span id="cart-badge">0</span>
        const badge = document.getElementById('cart-badge');
        if (badge) {
            badge.textContent = totalItems;
        }
    }

    // Attach event listeners to all add-to-cart buttons
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('add-btn')) {
            const button = event.target;
            const itemId = button.getAttribute('data-id');
            const itemName = button.getAttribute('data-name');
            const itemPrice = button.getAttribute('data-price');

            addToCart(itemId, itemName, itemPrice);
        }
    });

    // Initialize cart badge on page load
    updateCartBadge();
});
