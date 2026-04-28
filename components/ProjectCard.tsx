"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Play, ExternalLink } from "lucide-react";

interface ProjectCardProps {
    project: {
        _id: string;
        title: string;
        category: string;
        thumbnail: string;
        description: string;
    };
}

export default function ProjectCard({ project }: ProjectCardProps) {
    return (
        <motion.div
            layout
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            whileHover={{ y: -10 }}
            className="group relative"
        >
            <Link href={`/portfolio/${project._id}`}>
                <div className="relative aspect-[4/3] rounded-2xl overflow-hidden glass-card">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                        src={project.thumbnail}
                        alt={project.title}
                        className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                    />
                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                        <div className="w-12 h-12 rounded-full bg-amber-500 flex items-center justify-center translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
                            <Play size={20} className="text-black fill-current" />
                        </div>
                    </div>
                    <div className="absolute top-4 left-4 z-20">
                        <span className="px-3 py-1 bg-black/50 backdrop-blur-md rounded-full text-[10px] uppercase tracking-wider font-bold border border-white/10">
                            {project.category}
                        </span>
                    </div>
                </div>

                <div className="mt-4 px-2">
                    <div className="flex justify-between items-start">
                        <h3 className="text-xl font-bold font-space tracking-tight group-hover:text-amber-500 transition-colors">
                            {project.title}
                        </h3>
                        <ExternalLink size={16} className="text-gray-500 group-hover:text-white" />
                    </div>
                    <p className="text-gray-400 text-sm mt-1 line-clamp-2 leading-relaxed">
                        {project.description}
                    </p>
                </div>
            </Link>
        </motion.div>
    );
}
