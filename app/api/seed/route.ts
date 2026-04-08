import { NextResponse } from "next/server";
import connectDB from "@/lib/mongodb";
import Admin from "@/lib/models/Admin";
import bcrypt from "bcryptjs";

export async function GET() {
    try {
        await connectDB();

        const email = process.env.ADMIN_EMAIL || "akash@neupane.com";
        const password = process.env.ADMIN_PASSWORD || "Admin@1234";

        const existingAdmin = await Admin.findOne({ email });
        if (existingAdmin) {
            return NextResponse.json({ message: "Admin already exists" });
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        await Admin.create({
            email,
            password: hashedPassword
        });

        return NextResponse.json({
            message: "Admin created successfully",
            email: email,
            status: "SUCCESS"
        });
    } catch (error) {
        console.error("Seed Error:", error);
        return NextResponse.json({ error: "Seed failed" }, { status: 500 });
    }
}
