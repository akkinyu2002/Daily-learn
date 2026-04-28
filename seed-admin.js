const bcrypt = require('bcryptjs');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const path = require('path');

// Load env from .env.local
dotenv.config({ path: path.join(__dirname, '.env.local') });

const MONGODB_URI = process.env.MONGODB_URI;

if (!MONGODB_URI) {
    console.error('Please define MONGODB_URI in .env.local');
    process.exit(1);
}

const AdminSchema = new mongoose.Schema({
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    createdAt: { type: Date, default: Date.now }
});

const Admin = mongoose.models.Admin || mongoose.model('Admin', AdminSchema);

async function seed() {
    try {
        await mongoose.connect(MONGODB_URI);
        console.log('Connected to MongoDB');

        const email = process.env.ADMIN_EMAIL || 'akash@neupane.com';
        const password = process.env.ADMIN_PASSWORD || 'Admin@1234';

        const existingAdmin = await Admin.findOne({ email });
        if (existingAdmin) {
            console.log('Admin already exists');
        } else {
            const hashedPassword = await bcrypt.hash(password, 10);
            await Admin.create({
                email,
                password: hashedPassword
            });
            console.log('Admin created successfully');
            console.log('Email:', email);
            console.log('Password:', password);
        }
    } catch (err) {
        console.error('Seed error:', err);
    } finally {
        await mongoose.disconnect();
        process.exit(0);
    }
}

seed();
