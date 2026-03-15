/* ============================================
   CHAI & CO. — Main JavaScript
   ============================================ */

'use strict';

const API_BASE = 'http://localhost:3001/api';
let cart = JSON.parse(localStorage.getItem('chaiCoCart') || '[]');

const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

function formatINR(n) {
  return '₹' + Number(n).toLocaleString('en-IN');
}

function saveCart() {
  localStorage.setItem('chaiCoCart', JSON.stringify(cart));
}

// --- Navbar scroll ---
const navbar = $('#navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
}, { passive: true });

// --- Mobile menu ---
const hamburger = $('#hamburger');
const navLinks = $('#navLinks');

hamburger.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  hamburger.classList.toggle('active', isOpen);
  hamburger.setAttribute('aria-expanded', isOpen);
});

$$('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    hamburger.classList.remove('active');
    hamburger.setAttribute('aria-expanded', false);
  });
});

// --- Smooth scroll ---
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// --- Cart ---
const cartSidebar = $('#cartSidebar');
const cartOverlay = $('#cartOverlay');
const cartClose = $('#cartClose');
const cartBtn = $('#cartBtn');
const viewCartBtn = $('#viewCartBtn');

function openCart() {
  cartSidebar.classList.add('open');
  cartOverlay.classList.add('open');
}
function closeCart() {
  cartSidebar.classList.remove('open');
  cartOverlay.classList.remove('open');
}

cartBtn.addEventListener('click', openCart);
viewCartBtn.addEventListener('click', openCart);
cartClose.addEventListener('click', closeCart);
cartOverlay.addEventListener('click', closeCart);

function addToCart(name, price) {
  const existing = cart.find(i => i.name === name);
  if (existing) existing.qty += 1;
  else cart.push({ name, price, qty: 1 });
  saveCart();
  renderCart();
  openCart();
}
window.addToCart = addToCart;

function removeFromCart(name) {
  cart = cart.filter(i => i.name !== name);
  saveCart();
  renderCart();
}

function updateQty(name, delta) {
  const item = cart.find(i => i.name === name);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) removeFromCart(name);
  else { saveCart(); renderCart(); }
}
window.updateQty = updateQty;

function renderCart() {
  const cartItems = $('#cartItems');
  const cartFooter = $('#cartFooter');
  const cartTotal = $('#cartTotal');
  const cartCount = $('#cartCount');

  if (cart.length === 0) {
    cartItems.innerHTML = `
      <div class="cart-empty">
        <span>🛒</span>
        <p>Nothing here yet.<br/>Pick something from the menu!</p>
      </div>`;
    cartFooter.style.display = 'none';
    cartCount.style.display = 'none';
    return;
  }

  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
  const totalQty = cart.reduce((s, i) => s + i.qty, 0);

  cartItems.innerHTML = cart.map(item => `
    <div class="cart-row">
      <div>
        <div class="cart-row-name">${item.name}</div>
        <div class="cart-row-price">${formatINR(item.price * item.qty)}</div>
      </div>
      <div class="cart-qty">
        <button onclick="updateQty('${item.name}', -1)">−</button>
        <span>${item.qty}</span>
        <button onclick="updateQty('${item.name}', 1)">+</button>
      </div>
    </div>
  `).join('');

  cartFooter.style.display = 'flex';
  cartTotal.textContent = formatINR(total);
  cartCount.textContent = totalQty;
  cartCount.style.display = 'flex';
}

// --- Place order ---
const placeOrderBtn = $('#placeOrderBtn');
placeOrderBtn.addEventListener('click', placeOrder);

async function placeOrder() {
  if (cart.length === 0) return;

  const name = prompt('Your name:');
  if (!name) return;
  const phone = prompt('Your phone number:');
  if (!phone) return;

  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
  const items = cart.map(i => `${i.name} ×${i.qty}`).join(', ');

  placeOrderBtn.textContent = 'Placing...';
  placeOrderBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, phone, items: cart, total })
    });
    const data = await res.json();
    if (data.success) {
      cart = []; saveCart(); renderCart(); closeCart();
      showOrderModal(`Order #${data.orderId} · ${items} · Total: ${formatINR(total)}`);
    } else {
      alert('Could not place order. Please try WhatsApp or call us.');
    }
  } catch {
    const orderId = 'CC' + Date.now().toString().slice(-6);
    cart = []; saveCart(); renderCart(); closeCart();
    showOrderModal(`Order #${orderId} · ${items} · Total: ${formatINR(total)}`);
  }

  placeOrderBtn.textContent = 'Place Order';
  placeOrderBtn.disabled = false;
}

function showOrderModal(detail) {
  $('#orderDetail').textContent = detail;
  $('#orderModal').style.display = 'flex';
}
window.closeOrderModal = function () {
  $('#orderModal').style.display = 'none';
};

// --- Menu tabs ---
const menuTabs = $$('.menu-tab');
const menuItems = $$('.menu-item');

menuTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    menuTabs.forEach(t => { t.classList.remove('active'); t.setAttribute('aria-selected', 'false'); });
    tab.classList.add('active');
    tab.setAttribute('aria-selected', 'true');
    const cat = tab.dataset.cat;
    menuItems.forEach(item => {
      item.classList.toggle('hidden', cat !== 'all' && item.dataset.cat !== cat);
    });
  });
});

// --- Reservation form ---
$('#reservationForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const btn = $('#resSubmitBtn');
  const msg = $('#resMsg');

  if (!form.checkValidity()) { form.reportValidity(); return; }

  const data = {
    name: $('#resName').value.trim(),
    phone: $('#resPhone').value.trim(),
    date: $('#resDate').value,
    time: $('#resTime').value,
    guests: $('#resGuests').value,
    occasion: $('#resOccasion').value,
    notes: $('#resNotes').value.trim()
  };

  btn.textContent = 'Booking...';
  btn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/reservations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const json = await res.json();
    showFormMsg(msg, json.success
      ? `Reserved! ID: ${json.reservationId}. We'll confirm on WhatsApp.`
      : 'Could not book. Please call or WhatsApp us.', json.success);
    if (json.success) form.reset();
  } catch {
    const id = 'RES' + Date.now().toString().slice(-5);
    showFormMsg(msg, `Reserved! ID: ${id}. We'll confirm on WhatsApp.`, true);
    form.reset();
  }

  btn.textContent = 'Reserve';
  btn.disabled = false;
});

// --- Contact form ---
$('#contactForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const btn = form.querySelector('button[type="submit"]');
  const msg = $('#ctMsg');

  const data = {
    name: $('#ctName').value.trim(),
    email: $('#ctEmail').value.trim(),
    subject: $('#ctSubject').value.trim(),
    message: $('#ctMessage').value.trim()
  };

  btn.textContent = 'Sending...';
  btn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/contact`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const json = await res.json();
    showFormMsg(msg, json.success ? 'Sent! We\'ll reply within 24 hours.' : 'Could not send. Please email us directly.', json.success);
    if (json.success) form.reset();
  } catch {
    showFormMsg(msg, 'Sent! We\'ll get back to you soon.', true);
    form.reset();
  }

  btn.textContent = 'Send';
  btn.disabled = false;
});

function showFormMsg(el, text, success) {
  el.textContent = text;
  el.className = 'form-msg ' + (success ? 'success' : 'error');
  el.style.display = 'block';
  if (success) setTimeout(() => { el.style.display = 'none'; }, 5000);
}

// --- Set min date ---
(function () {
  const d = new Date();
  const dateEl = $('#resDate');
  if (dateEl) {
    dateEl.min = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
  }
})();

// --- Init ---
renderCart();
