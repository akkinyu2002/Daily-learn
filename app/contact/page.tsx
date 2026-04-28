"use client";

import { motion } from "framer-motion";
import { Mail, Phone, MapPin, Instagram, Linkedin, MessageCircle, Send } from "lucide-react";

export default function ContactPage() {
    return (
        <div className="pt-32 pb-24 min-h-screen">
            <div className="container mx-auto px-6">
                <header className="mb-16">
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-4xl md:text-7xl font-bold font-space tracking-tighter mb-6"
                    >
                        Let's <span className="text-amber-500 italic">Connect</span>.
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.2 }}
                        className="text-gray-400 max-w-xl text-lg"
                    >
                        I'm currently available for freelance work and full-time opportunities.
                        Have a project in mind? Reach out!
                    </motion.p>
                </header>

                <div className="flex flex-col lg:flex-row gap-16">
                    <div className="w-full lg:w-1/2">
                        <form className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <label className="text-xs uppercase tracking-widest font-bold text-gray-500">Your Name</label>
                                    <input type="text" className="w-full bg-white/5 border border-white/5 rounded-2xl px-6 py-4 focus:outline-none focus:border-amber-500 transition-colors" placeholder="Akash Neupane" />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs uppercase tracking-widest font-bold text-gray-500">Email Address</label>
                                    <input type="email" className="w-full bg-white/5 border border-white/5 rounded-2xl px-6 py-4 focus:outline-none focus:border-amber-500 transition-colors" placeholder="akash@example.com" />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs uppercase tracking-widest font-bold text-gray-500">Subject</label>
                                <input type="text" className="w-full bg-white/5 border border-white/5 rounded-2xl px-6 py-4 focus:outline-none focus:border-amber-500 transition-colors" placeholder="Project Inquiry" />
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs uppercase tracking-widest font-bold text-gray-500">Message</label>
                                <textarea rows={6} className="w-full bg-white/5 border border-white/5 rounded-2xl px-6 py-4 focus:outline-none focus:border-amber-500 transition-colors" placeholder="Let's build something amazing together..."></textarea>
                            </div>

                            <button type="button" className="group flex items-center justify-center w-full md:w-auto px-12 py-5 bg-amber-500 text-black font-bold rounded-full hover:bg-white transition-all">
                                Send Message
                                <Send className="ml-2 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" size={18} />
                            </button>
                        </form>
                    </div>

                    <div className="w-full lg:w-1/2">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <div className="p-8 glass-card rounded-3xl">
                                <div className="w-12 h-12 rounded-2xl bg-amber-500/10 flex items-center justify-center text-amber-500 mb-6">
                                    <Mail size={24} />
                                </div>
                                <h4 className="font-bold font-space text-white mb-2">Email</h4>
                                <p className="text-sm text-gray-400 break-all">akashneupane@example.com</p>
                            </div>

                            <div className="p-8 glass-card rounded-3xl">
                                <div className="w-12 h-12 rounded-2xl bg-amber-500/10 flex items-center justify-center text-amber-500 mb-6">
                                    <Phone size={24} />
                                </div>
                                <h4 className="font-bold font-space text-white mb-2">Phone</h4>
                                <p className="text-sm text-gray-400">+977 9860212330</p>
                            </div>

                            <div className="p-8 glass-card rounded-3xl">
                                <div className="w-12 h-12 rounded-2xl bg-amber-500/10 flex items-center justify-center text-amber-500 mb-6">
                                    <MapPin size={24} />
                                </div>
                                <h4 className="font-bold font-space text-white mb-2">Location</h4>
                                <p className="text-sm text-gray-400">Johang, Gulmi, Nepal</p>
                            </div>

                            <div className="p-8 glass-card rounded-3xl">
                                <div className="w-12 h-12 rounded-2xl bg-amber-500/10 flex items-center justify-center text-amber-500 mb-6">
                                    <Linkedin size={24} />
                                </div>
                                <h4 className="font-bold font-space text-white mb-2">Social Hub</h4>
                                <div className="flex space-x-4">
                                    <a href="#" className="p-2 bg-white/5 rounded-lg text-gray-400 hover:text-white transition-colors">
                                        <Instagram size={18} />
                                    </a>
                                    <a href="#" className="p-2 bg-white/5 rounded-lg text-gray-400 hover:text-white transition-colors">
                                        <Linkedin size={18} />
                                    </a>
                                    <a href="https://wa.me/9779860212330" className="p-2 bg-white/5 rounded-lg text-gray-400 hover:text-white transition-colors">
                                        <MessageCircle size={18} />
                                    </a>
                                </div>
                            </div>
                        </div>

                        <div className="mt-8 p-8 border border-white/5 bg-gradient-to-br from-amber-500/5 to-transparent rounded-3xl">
                            <p className="text-gray-400 italic">
                                "Visual storytelling is the most powerful way to connect a brand with its audience. Let's make your story unforgettable."
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
