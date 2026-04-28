/**
 * CHAI & CO. — Backend Server
 * Express REST API for orders, reservations, contact
 * 
 * Start with: node server.js
 * Runs on:    http://localhost:3001
 */

const express = require('express');
const cors    = require('cors');
const fs      = require('fs');
const path    = require('path');

const app  = express();
const PORT = process.env.PORT || 3001;
const DB_PATH = path.join(__dirname, 'db', 'data.json');

// ─── MIDDLEWARE ───
app.use(cors({ origin: '*' }));
app.use(express.json());
app.use(express.static(path.join(__dirname, '..'))); // Serve frontend

// ─── DB HELPERS ───
function readDB() {
  try {
    return JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));
  } catch {
    return { orders: [], reservations: [], contacts: [] };
  }
}

function writeDB(data) {
  fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2), 'utf8');
}

function genId(prefix = 'ID') {
  return prefix + Date.now().toString(36).toUpperCase() + Math.random().toString(36).slice(2, 5).toUpperCase();
}

// ─── ROUTES ───

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', cafe: 'Chai & Co.', time: new Date().toISOString() });
});

// GET menu (static data)
app.get('/api/menu', (req, res) => {
  res.json({
    success: true,
    menu: [
      // Hyderabad Faves
      { id: 'hyd-1', cat: 'hyd', name: 'Irani Chai',             price: 49,  veg: true  },
      { id: 'hyd-2', cat: 'hyd', name: 'Bun Maska',              price: 39,  veg: true  },
      { id: 'hyd-3', cat: 'hyd', name: 'Osmania Biscuits (6pc)', price: 49,  veg: true  },
      { id: 'hyd-4', cat: 'hyd', name: 'Chai + Bun Combo',       price: 79,  veg: true  },
      { id: 'hyd-5', cat: 'hyd', name: 'Double Ka Meetha Shake', price: 149, veg: true  },
      // Coffee
      { id: 'cof-1', cat: 'coffee', name: 'Espresso',            price: 99,  veg: true  },
      { id: 'cof-2', cat: 'coffee', name: 'Americano',           price: 129, veg: true  },
      { id: 'cof-3', cat: 'coffee', name: 'Cappuccino',          price: 149, veg: true  },
      { id: 'cof-4', cat: 'coffee', name: 'Flat White',          price: 159, veg: true  },
      { id: 'cof-5', cat: 'coffee', name: 'Cold Coffee',         price: 169, veg: true  },
      { id: 'cof-6', cat: 'coffee', name: 'Cold Brew',           price: 179, veg: true  },
      { id: 'cof-7', cat: 'coffee', name: 'Dalgona Coffee',      price: 169, veg: true  },
      // Bites
      { id: 'bit-1', cat: 'bites', name: 'Chicken Shawarma',     price: 179, veg: false },
      { id: 'bit-2', cat: 'bites', name: 'Falafel Shawarma',     price: 149, veg: true  },
      { id: 'bit-3', cat: 'bites', name: 'Smash Burger',         price: 219, veg: false },
      { id: 'bit-4', cat: 'bites', name: 'Crispy Veg Burger',    price: 169, veg: true  },
      { id: 'bit-5', cat: 'bites', name: 'Chicken Momos (8pc)',  price: 179, veg: false },
      { id: 'bit-6', cat: 'bites', name: 'Veg Momos (8pc)',      price: 149, veg: true  },
      { id: 'bit-7', cat: 'bites', name: 'Loaded Fries',         price: 179, veg: true  },
      { id: 'bit-8', cat: 'bites', name: 'Cheesy Fries',         price: 159, veg: true  },
      { id: 'bit-9', cat: 'bites', name: 'Chicken Tikka Sandwich', price: 199, veg: false },
      { id: 'bit-10',cat: 'bites', name: 'Club Sandwich',        price: 189, veg: true  },
      // Desserts
      { id: 'des-1', cat: 'desserts', name: 'NY Cheesecake',     price: 149, veg: true  },
      { id: 'des-2', cat: 'desserts', name: 'Chocolate Brownie', price: 99,  veg: true  },
      { id: 'des-3', cat: 'desserts', name: 'Butter Croissant',  price: 99,  veg: true  },
      { id: 'des-4', cat: 'desserts', name: 'Seasonal Pastry',   price: 119, veg: true  },
      // Specials
      { id: 'spc-1', cat: 'specials', name: 'Hyd Smash Box',     price: 449, veg: false },
      { id: 'spc-2', cat: 'specials', name: 'Chai & Chai Combo', price: 119, veg: true  },
      { id: 'spc-3', cat: 'specials', name: 'Full Monty Brunch', price: 449, veg: true  },
    ]
  });
});

// POST order
app.post('/api/orders', (req, res) => {
  const { name, phone, items, total } = req.body;

  if (!name || !phone || !items || !Array.isArray(items) || items.length === 0) {
    return res.status(400).json({ success: false, error: 'Missing required fields' });
  }

  const db = readDB();
  const order = {
    orderId:   genId('CC'),
    name:      name.trim(),
    phone:     phone.trim(),
    items,
    total,
    status:    'received',
    createdAt: new Date().toISOString()
  };

  db.orders.push(order);
  writeDB(db);

  console.log(`\n🛒 NEW ORDER [${order.orderId}] from ${order.name} (${order.phone})`);
  console.log(`   Items: ${items.map(i => `${i.name} ×${i.qty}`).join(', ')}`);
  console.log(`   Total: ₹${total}`);

  res.status(201).json({ success: true, orderId: order.orderId, message: 'Order received!' });
});

// GET all orders (admin)
app.get('/api/orders', (req, res) => {
  const db = readDB();
  res.json({ success: true, count: db.orders.length, orders: db.orders });
});

// PATCH order status
app.patch('/api/orders/:id/status', (req, res) => {
  const { id } = req.params;
  const { status } = req.body;
  const validStatuses = ['received', 'preparing', 'ready', 'out-for-delivery', 'delivered', 'cancelled'];

  if (!validStatuses.includes(status)) {
    return res.status(400).json({ success: false, error: 'Invalid status' });
  }

  const db = readDB();
  const order = db.orders.find(o => o.orderId === id);
  if (!order) return res.status(404).json({ success: false, error: 'Order not found' });

  order.status = status;
  order.updatedAt = new Date().toISOString();
  writeDB(db);

  res.json({ success: true, order });
});

// POST reservation
app.post('/api/reservations', (req, res) => {
  const { name, phone, date, time, guests, occasion, notes } = req.body;

  if (!name || !phone || !date || !time || !guests) {
    return res.status(400).json({ success: false, error: 'Missing required fields' });
  }

  const db = readDB();
  const reservation = {
    reservationId: genId('RES'),
    name:     name.trim(),
    phone:    phone.trim(),
    date,
    time,
    guests:   parseInt(guests),
    occasion: occasion || '',
    notes:    notes || '',
    status:   'confirmed',
    createdAt: new Date().toISOString()
  };

  db.reservations.push(reservation);
  writeDB(db);

  console.log(`\n📅 RESERVATION [${reservation.reservationId}]`);
  console.log(`   ${reservation.name} · ${reservation.guests} guests · ${reservation.date} ${reservation.time}`);
  if (occasion) console.log(`   Occasion: ${occasion}`);

  res.status(201).json({
    success: true,
    reservationId: reservation.reservationId,
    message: 'Reservation confirmed!'
  });
});

// GET all reservations (admin)
app.get('/api/reservations', (req, res) => {
  const db = readDB();
  res.json({ success: true, count: db.reservations.length, reservations: db.reservations });
});

// POST contact message
app.post('/api/contact', (req, res) => {
  const { name, email, subject, message } = req.body;

  if (!name || !email || !message) {
    return res.status(400).json({ success: false, error: 'Missing required fields' });
  }

  const db = readDB();
  const contact = {
    id:        genId('MSG'),
    name:      name.trim(),
    email:     email.trim(),
    subject:   subject || 'No subject',
    message:   message.trim(),
    createdAt: new Date().toISOString()
  };

  db.contacts.push(contact);
  writeDB(db);

  console.log(`\n✉️  CONTACT from ${contact.name} <${contact.email}>`);
  console.log(`   Subject: ${contact.subject}`);

  res.status(201).json({ success: true, message: 'Message received!' });
});

// ─── 404 ───
app.use((req, res) => {
  res.status(404).json({ success: false, error: 'Route not found' });
});

// ─── START ───
app.listen(PORT, () => {
  console.log(`\n☕ Chai & Co. Backend running on http://localhost:${PORT}`);
  console.log(`   API docs:`);
  console.log(`   GET  /api/health`);
  console.log(`   GET  /api/menu`);
  console.log(`   POST /api/orders`);
  console.log(`   POST /api/reservations`);
  console.log(`   POST /api/contact`);
  console.log(`   GET  /api/orders       (admin)`);
  console.log(`   GET  /api/reservations (admin)`);
  console.log(`\n   Frontend: http://localhost:${PORT}/index.html\n`);
});
