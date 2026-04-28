"use client";

import { useSession, signOut } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import {
    Plus,
    LayoutDashboard,
    Video,
    Palette,
    Briefcase,
    LogOut,
    ArrowUpRight,
    ExternalLink
} from "lucide-react";

export default function AdminDashboard() {
    const { data: session, status } = useSession();
    const router = useRouter();
    const [stats, setStats] = useState({
        total: 0,
        video: 0,
        design: 0,
        motion: 0
    });

    useEffect(() => {
        if (status === "unauthenticated") {
            router.push("/admin/login");
        }

        if (status === "authenticated") {
            fetch("/api/projects")
                .then(res => res.json())
                .then(data => {
                    setStats({
                        total: data.length,
                        video: data.filter(p => p.category === "Video Editing").length,
                        design: data.filter(p => p.category === "Graphic Design").length,
                        motion: data.filter(p => p.category === "Motion Graphics").length
                    });
                });
        }
    }, [status, router]);

    if (status === "loading") {
        return (
            <div className="min-h-screen flex items-center justify-center bg-[#0a0a0a]">
                <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0a0a0a] pt-24 pb-12">
            <div className="container mx-auto px-6">
                <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-6">
                    <div>
                        <h1 className="text-3xl font-bold font-space flex items-center gap-3">
                            <LayoutDashboard className="text-amber-500" />
                            Dashboard
                        </h1>
                        <p className="text-gray-500 text-sm mt-1">Logged in as {session?.user?.email}</p>
                    </div>

                    <div className="flex items-center gap-4">
                        <Link
                            href="/admin/projects"
                            className="flex items-center px-6 py-3 bg-white text-black font-bold rounded-full hover:bg-amber-500 transition-all text-sm"
                        >
                            <Plus size={18} className="mr-2" />
                            New Project
                        </Link>
                        <button
                            onClick={() => signOut()}
                            className="flex items-center px-6 py-3 bg-white/5 border border-white/10 text-white rounded-full hover:bg-white/10 transition-all text-sm"
                        >
                            <LogOut size={18} className="mr-2" />
                            Logout
                        </button>
                    </div>
                </header>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
                    {[
                        { label: "Total Projects", value: stats.total, icon: Briefcase, color: "blue" },
                        { label: "Video Editing", value: stats.video, icon: Video, color: "amber" },
                        { label: "Graphic Design", value: stats.design, icon: Palette, color: "purple" },
                        { label: "Motion Graphics", value: stats.motion, icon: ArrowUpRight, color: "green" }
                    ].map((stat, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.1 }}
                            className="p-8 rounded-3xl glass-card border-white/5"
                        >
                            <div className={`w-12 h-12 rounded-2xl bg-${stat.color}-500/10 flex items-center justify-center text-${stat.color}-500 mb-6`}>
                                <stat.icon size={24} />
                            </div>
                            <h3 className="text-gray-500 text-sm font-bold uppercase tracking-widest mb-1">{stat.label}</h3>
                            <p className="text-4xl font-bold font-space">{stat.value}</p>
                        </motion.div>
                    ))}
                </div>

                {/* Quick Actions / Recent Activity */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div className="p-8 rounded-3xl glass-card border-white/5">
                        <h3 className="text-xl font-bold font-space mb-6 flex items-center justify-between">
                            Quick Links
                            <ExternalLink size={18} className="text-gray-700" />
                        </h3>
                        <div className="space-y-4">
                            <Link href="/" target="_blank" className="flex items-center justify-between p-4 bg-white/5 rounded-2xl hover:bg-white/10 transition-all group">
                                <span className="text-sm">View Website</span>
                                <ArrowUpRight size={16} className="text-gray-500 group-hover:text-amber-500 transition-colors" />
                            </Link>
                            <Link href="/portfolio" target="_blank" className="flex items-center justify-between p-4 bg-white/5 rounded-2xl hover:bg-white/10 transition-all group">
                                <span className="text-sm">Public Portfolio</span>
                                <ArrowUpRight size={16} className="text-gray-500 group-hover:text-amber-500 transition-colors" />
                            </Link>
                        </div>
                    </div>

                    <div className="p-8 rounded-3xl glass-card border-amber-500/10 bg-gradient-to-br from-amber-500/5 to-transparent">
                        <h3 className="text-xl font-bold font-space mb-4">Welcome back, Akash!</h3>
                        <p className="text-gray-500 text-sm leading-relaxed mb-6">
                            Your portfolio is looking great. Keep uploading your latest creative pieces to stay relevant and attract new clients.
                        </p>
                        <div className="flex space-x-2">
                            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                            <span className="text-[10px] uppercase tracking-widest font-bold text-gray-400">System Online</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
