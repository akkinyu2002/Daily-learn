"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight, Play } from "lucide-react";

export default function HeroSection() {
    return (
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
            {/* Background elements */}
            <div className="absolute inset-0 z-0">
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-amber-500/10 rounded-full blur-[120px]" />
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-[120px]" />
            </div>

            <div className="container mx-auto px-6 relative z-10 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                >
                    <span className="inline-block px-4 py-1.5 mb-6 text-xs font-semibold tracking-widest text-amber-500 uppercase bg-amber-500/10 rounded-full">
                        Video Editor & Graphic Designer
                    </span>
                    <h1 className="text-5xl md:text-8xl font-bold font-space tracking-tighter mb-6 bg-clip-text text-transparent bg-gradient-to-b from-white to-white/50">
                        Akash Neupane
                    </h1>
                    <p className="text-lg md:text-2xl text-gray-400 max-w-2xl mx-auto mb-10 font-inter leading-relaxed">
                        Crafting visual stories through <span className="text-white font-medium">motion</span> and <span className="text-white font-medium">design</span>.
                    </p>

                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <Link
                            href="/portfolio"
                            className="group flex items-center px-8 py-4 bg-white text-black font-semibold rounded-full hover:bg-amber-500 transition-all"
                        >
                            View Portfolio
                            <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={20} />
                        </Link>

                        <button className="flex items-center px-8 py-4 bg-white/5 border border-white/10 hover:bg-white/10 rounded-full transition-all">
                            <span className="w-8 h-8 rounded-full bg-amber-500 items-center justify-center flex mr-3">
                                <Play size={14} className="text-black fill-current" />
                            </span>
                            Watch Reel
                        </button>
                    </div>
                </motion.div>
            </div>

            {/* Decorative vertical lines */}
            <div className="absolute bottom-0 left-12 w-px h-24 bg-gradient-to-t from-white/20 to-transparent" />
            <div className="absolute bottom-0 right-12 w-px h-24 bg-gradient-to-t from-white/20 to-transparent" />
        </section>
    );
}
