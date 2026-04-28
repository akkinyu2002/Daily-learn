"use client";

import { useState, useEffect } from "react";

export default function Footer() {
    const [year, setYear] = useState(2025);

    useEffect(() => {
        setYear(new Date().getFullYear());
    }, []);

    return (
        <footer className="py-12 border-t border-white/5 bg-[#0a0a0a]">
            <div className="container mx-auto px-6">
                <div className="flex flex-col md:flex-row justify-between items-center bg-transparent">
                    <div className="mb-6 md:mb-0">
                        <h2 className="text-xl font-bold font-space tracking-tighter mb-2">
                            AAKASH<span className="text-amber-500">.</span>
                        </h2>
                        <p className="text-gray-500 text-sm max-w-xs">
                            Crafting visual stories through motion and design.
                            Let's create something extraordinary together.
                        </p>
                    </div>

                    <div className="flex flex-col items-center md:items-end space-y-4">
                        <div className="flex space-x-6">
                            <a href="/portfolio" className="text-sm text-gray-400 hover:text-white transition-colors">Work</a>
                            <a href="/about" className="text-sm text-gray-400 hover:text-white transition-colors">About</a>
                            <a href="/contact" className="text-sm text-gray-400 hover:text-white transition-colors">Contact</a>
                        </div>
                        <p className="text-gray-600 text-xs">
                            Copyright © {year} Aakash Neupane. All Rights Reserved.
                        </p>
                    </div>
                </div>
            </div>
        </footer>
    );
}
