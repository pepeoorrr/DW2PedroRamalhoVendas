// Configuração da API
const API_URL = 'http://localhost:8000';

// Carrinho
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let products = [];

// Função para fazer requisições à API
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição:', error);
        throw error;
    }
}

// Funções do carrinho
function updateCartCount() {
    const count = cart.reduce((total, item) => total + item.quantity, 0);
    document.getElementById('cart-count').textContent = count;
}

function updateCartTotal() {
    let subtotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    let discount = 0;
    
    const couponInput = document.getElementById('coupon-input');
    if (couponInput.value === 'ALUNO10') {
        discount = subtotal * 0.1;
    }
    
    const total = subtotal - discount;
    
    document.getElementById('cart-subtotal').textContent = `R$ ${subtotal.toFixed(2)}`;
    document.getElementById('cart-discount').textContent = `R$ ${discount.toFixed(2)}`;
    document.getElementById('cart-total').textContent = `R$ ${total.toFixed(2)}`;
}

function addToCart(product) {
    if (product.stock === 0) {
        alert('Produto fora de estoque');
        return;
    }
    
    const cartItem = cart.find(item => item.id === product.id);
    if (cartItem) {
        if (cartItem.quantity < product.stock) {
            cartItem.quantity++;
        } else {
            alert('Quantidade máxima atingida');
            return;
        }
    } else {
        cart.push({ ...product, quantity: 1 });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    renderCart();
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    renderCart();
}

function updateCartQuantity(productId, delta) {
    const cartItem = cart.find(item => item.id === productId);
    const product = products.find(p => p.id === productId);
    
    if (cartItem) {
        const newQuantity = cartItem.quantity + delta;
        if (newQuantity > 0 && newQuantity <= product.stock) {
            cartItem.quantity = newQuantity;
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartCount();
            renderCart();
        }
    }
}

function renderCart() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div>
                <h3>${item.name}</h3>
                <p>R$ ${item.price.toFixed(2)} x ${item.quantity}</p>
            </div>
            <div>
                <button onclick="updateCartQuantity(${item.id}, -1)">-</button>
                <span>${item.quantity}</span>
                <button onclick="updateCartQuantity(${item.id}, 1)">+</button>
                <button onclick="removeFromCart(${item.id})">🗑️</button>
            </div>
        </div>
    `).join('');
    
    updateCartTotal();
}

// Funções de produtos
async function loadProducts() {
    try {
        products = await fetchAPI('/products');
        renderProducts(products);
    } catch (error) {
        console.error('Erro ao carregar produtos:', error);
    }
}

function renderProducts(productsToRender) {
    const grid = document.getElementById('products-grid');
    grid.innerHTML = productsToRender.map(product => `
        <div class="product-card">
            <img src="${product.image || 'https://via.placeholder.com/200'}" alt="${product.name}">
            <div class="product-info">
                <h3>${product.name}</h3>
                <p>${product.description || ''}</p>
                <p class="product-price">R$ ${product.price.toFixed(2)}</p>
                <p class="product-stock">${product.stock} em estoque</p>
                <button onclick="addToCart(${JSON.stringify(product)})"
                        ${product.stock === 0 ? 'disabled' : ''}
                        aria-label="Adicionar ${product.name} ao carrinho">
                    Adicionar ao carrinho
                </button>
            </div>
        </div>
    `).join('');
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Carregar produtos
    loadProducts();
    updateCartCount();
    
    // Botão do carrinho
    const cartButton = document.getElementById('cart-button');
    const cartModal = document.getElementById('cart-modal');
    cartButton.addEventListener('click', () => {
        cartModal.setAttribute('aria-hidden', 'false');
        cartButton.setAttribute('aria-pressed', 'true');
        renderCart();
    });
    
    // Fechar carrinho
    document.getElementById('close-cart').addEventListener('click', () => {
        cartModal.setAttribute('aria-hidden', 'true');
        cartButton.setAttribute('aria-pressed', 'false');
    });
    
    // Aplicar cupom
    document.getElementById('apply-coupon').addEventListener('click', updateCartTotal);
    
    // Finalizar pedido
    document.getElementById('checkout-button').addEventListener('click', async () => {
        try {
            const response = await fetchAPI('/orders', {
                method: 'POST',
                body: JSON.stringify({
                    items: cart,
                    coupon: document.getElementById('coupon-input').value
                })
            });
            
            alert('Pedido realizado com sucesso!');
            cart = [];
            localStorage.removeItem('cart');
            updateCartCount();
            cartModal.setAttribute('aria-hidden', 'true');
            loadProducts(); // Recarrega produtos para atualizar estoque
        } catch (error) {
            alert('Erro ao finalizar pedido');
        }
    });
    
    // Ordenação
    document.getElementById('sort-name').addEventListener('click', (e) => {
        const isPressed = e.target.getAttribute('aria-pressed') === 'true';
        e.target.setAttribute('aria-pressed', !isPressed);
        const sorted = [...products].sort((a, b) => 
            isPressed ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name)
        );
        renderProducts(sorted);
    });
    
    document.getElementById('sort-price-asc').addEventListener('click', (e) => {
        const isPressed = e.target.getAttribute('aria-pressed') === 'true';
        e.target.setAttribute('aria-pressed', !isPressed);
        document.getElementById('sort-price-desc').setAttribute('aria-pressed', 'false');
        const sorted = [...products].sort((a, b) => isPressed ? b.price - a.price : a.price - b.price);
        renderProducts(sorted);
    });
    
    document.getElementById('sort-price-desc').addEventListener('click', (e) => {
        const isPressed = e.target.getAttribute('aria-pressed') === 'true';
        e.target.setAttribute('aria-pressed', !isPressed);
        document.getElementById('sort-price-asc').setAttribute('aria-pressed', 'false');
        const sorted = [...products].sort((a, b) => isPressed ? a.price - b.price : b.price - a.price);
        renderProducts(sorted);
    });
    
    // Busca
    document.getElementById('search-input').addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filtered = products.filter(product => 
            product.name.toLowerCase().includes(searchTerm)
        );
        renderProducts(filtered);
    });
    
    // Admin
    const adminLink = document.getElementById('admin-link');
    const adminModal = document.getElementById('admin-modal');
    const productForm = document.getElementById('product-form');
    
    adminLink.addEventListener('click', (e) => {
        e.preventDefault();
        adminModal.setAttribute('aria-hidden', 'false');
    });
    
    document.getElementById('close-admin').addEventListener('click', () => {
        adminModal.setAttribute('aria-hidden', 'true');
    });
    
    productForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('product-name').value,
            description: document.getElementById('product-description').value,
            price: parseFloat(document.getElementById('product-price').value),
            stock: parseInt(document.getElementById('product-stock').value),
            category: document.getElementById('product-category').value,
            sku: document.getElementById('product-sku').value
        };
        
        try {
            await fetchAPI('/products', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
            
            alert('Produto cadastrado com sucesso!');
            productForm.reset();
            adminModal.setAttribute('aria-hidden', 'true');
            loadProducts();
        } catch (error) {
            alert('Erro ao cadastrar produto');
        }
    });
});
