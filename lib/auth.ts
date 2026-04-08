import { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import connectDB from "@/lib/mongodb";
import Admin from "@/lib/models/Admin";
import bcrypt from "bcryptjs";

export const authOptions: NextAuthOptions = {
    providers: [
        CredentialsProvider({
            name: "Credentials",
            credentials: {
                email: { label: "Email", type: "email" },
                password: { label: "Password", type: "password" }
            },
            async authorize(credentials) {
                if (!credentials?.email || !credentials?.password) {
                    throw new Error("Invalid credentials");
                }

                await connectDB();
                const admin = await Admin.findOne({ email: credentials.email });

                if (!admin) {
                    // For security, we might want a silent failure but for admin login usually explicit is fine
                    throw new Error("User not found");
                }

                const isValid = await bcrypt.compare(credentials.password, admin.password);

                if (!isValid) {
                    throw new Error("Incorrect password");
                }

                return {
                    id: admin._id.toString(),
                    email: admin.email,
                };
            }
        })
    ],
    session: {
        strategy: "jwt",
    },
    pages: {
        signIn: "/admin/login",
    },
    secret: process.env.NEXTAUTH_SECRET,
};
