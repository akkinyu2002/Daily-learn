"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X, Instagram, Linkedin, MessageCircle } from "lucide-react";

const links = [
    { name: "Home", href: "/" },
    { name: "Portfolio", href: "/portfolio" },
    { name: "About", href: "/about" },
    { name: "Contact", href: "/contact" },
];

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false);
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    return (
        <nav
            className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrolled ? "py-4 bg-[#0a0a0a]/80 backdrop-blur-md border-b border-white/5" : "py-6 bg-transparent"
                }`}
        >
            <div className="container mx-auto px-6 flex justify-between items-center">
                <Link href="/" className="text-xl font-bold font-space tracking-tighter">
                    AAKASH<span className="text-amber-500">.</span>
                </Link>

                {/* Desktop Menu */}
                <div className="hidden md:flex items-center space-x-8">
                    {links.map((link) => (
                        <Link
                            key={link.name}
                            href={link.href}
                            className="text-sm font-medium text-gray-400 hover:text-white transition-colors"
                        >
                            {link.name}
                        </Link>
                    ))}
                    <div className="flex items-center space-x-4 pl-4 border-l border-white/10">
                        <a href="https://instagram.com" target="_blank" className="text-gray-400 hover:text-amber-500 transition-colors">
                            <Instagram size={18} />
                        </a>
                        <a href="https://linkedin.com" target="_blank" className="text-gray-400 hover:text-amber-500 transition-colors">
                            <Linkedin size={18} />
                        </a>
                    </div>
                </div>

                {/* Mobile Toggle */}
                <button
                    className="md:hidden text-white focus:outline-none"
                    onClick={() => setIsOpen(!isOpen)}
                >
                    {isOpen ? <X size={24} /> : <Menu size={24} />}
                </button>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className="absolute top-full left-0 w-full bg-[#0a0a0a] border-b border-white/5 md:hidden"
                    >
                        <div className="flex flex-col p-6 space-y-4">
                            {links.map((link) => (
                                <Link
                                    key={link.name}
                                    href={link.href}
                                    onClick={() => setIsOpen(false)}
                                    className="text-lg font-medium text-gray-400 hover:text-white"
                                >
                                    {link.name}
                                </Link>
                            ))}
                            <div className="flex space-x-6 pt-4 border-t border-white/10">
                                <a href="https://instagram.com" target="_blank" className="text-gray-400">
                                    <Instagram size={20} />
                                </a>
                                <a href="https://linkedin.com" target="_blank" className="text-gray-400">
                                    <Linkedin size={20} />
                                </a>
                                <a href="https://wa.me/9779860212330" target="_blank" className="text-gray-400">
                                    <MessageCircle size={20} />
                                </a>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </nav>
    );
}
