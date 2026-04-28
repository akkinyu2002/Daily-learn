"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
    ArrowLeft,
    ExternalLink,
    Clock,
    User,
    Hammer,
    PlayCircle,
    ChevronLeft,
    ChevronRight
} from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";

export default function ProjectDetailsPage() {
    const { id } = useParams();
    const [project, setProject] = useState(null);
    const [loading, setLoading] = useState(true);
    const [activeImage, setActiveImage] = useState(0);

    useEffect(() => {
        fetch(`/api/projects/${id}`)
            .then(res => res.json())
            .then(data => {
                setProject(data);
                setLoading(false);
            })
            .catch(err => console.error(err));
    }, [id]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-[#0a0a0a]">
                <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    if (!project) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-[#0a0a0a]">
                <p className="text-gray-500">Project not found.</p>
            </div>
        );
    }

    const isVideo = project.category === "Video Editing" || (project.videoUrl && project.videoUrl.length > 0);

    return (
        <div className="pt-32 pb-24 min-h-screen">
            <div className="container mx-auto px-6">
                <Link href="/portfolio" className="inline-flex items-center text-gray-500 hover:text-white mb-12 transition-colors">
                    <ArrowLeft size={18} className="mr-2" />
                    Back to Portfolio
                </Link>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-16">
                    {/* Media Section */}
                    <div className="lg:col-span-8">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="rounded-3xl overflow-hidden glass-card bg-black shadow-2xl"
                        >
                            {isVideo ? (
                                <div className="aspect-video w-full">
                                    {/* Basic iframe for YouTube/Vimeo - in production would need better parsing */}
                                    <iframe
                                        className="w-full h-full"
                                        src={project.videoUrl?.replace("watch?v=", "embed/")}
                                        title={project.title}
                                        frameBorder="0"
                                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                        allowFullScreen
                                    ></iframe>
                                </div>
                            ) : (
                                <div className="relative aspect-video">
                                    {/* eslint-disable-next-line @next/next/no-img-element */}
                                    <img
                                        src={project.mediaUrls?.[activeImage] || project.thumbnail}
                                        alt={project.title}
                                        className="w-full h-full object-contain"
                                    />

                                    {project.mediaUrls?.length > 1 && (
                                        <div className="absolute inset-x-0 bottom-6 flex justify-center gap-2">
                                            {project.mediaUrls.map((_, i) => (
                                                <button
                                                    key={i}
                                                    onClick={() => setActiveImage(i)}
                                                    className={`w-2 h-2 rounded-full transition-all ${activeImage === i ? "bg-amber-500 w-8" : "bg-white/20"}`}
                                                />
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}
                        </motion.div>

                        <div className="mt-12">
                            <h1 className="text-3xl md:text-5xl font-bold font-space tracking-tight mb-6">{project.title}</h1>
                            <p className="text-gray-400 text-lg leading-relaxed">{project.description}</p>
                        </div>
                    </div>

                    {/* Details Sidebar */}
                    <div className="lg:col-span-4">
                        <div className="p-8 rounded-3xl glass-card space-y-8 sticky top-32">
                            <div>
                                <h4 className="text-xs uppercase tracking-widest font-bold text-gray-500 mb-4">Project Info</h4>
                                <div className="space-y-4">
                                    <div className="flex items-center gap-4">
                                        <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-amber-500">
                                            <User size={18} />
                                        </div>
                                        <div>
                                            <p className="text-[10px] uppercase text-gray-600 font-bold">Client</p>
                                            <p className="text-sm font-semibold">{project.client || "Personal Project"}</p>
                                        </div>
                                    </div>

                                    <div className="flex items-center gap-4">
                                        <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-amber-500">
                                            <Clock size={18} />
                                        </div>
                                        <div>
                                            <p className="text-[10px] uppercase text-gray-600 font-bold">Duration</p>
                                            <p className="text-sm font-semibold">{project.duration || "N/A"}</p>
                                        </div>
                                    </div>

                                    <div className="flex items-center gap-4">
                                        <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-amber-500">
                                            <Hammer size={18} />
                                        </div>
                                        <div className="flex-1">
                                            <p className="text-[10px] uppercase text-gray-600 font-bold">Tools Used</p>
                                            <div className="flex flex-wrap gap-1 mt-1">
                                                {project.toolsUsed?.map(tool => (
                                                    <span key={tool} className="text-[10px] px-2 py-0.5 bg-white/5 rounded-md">{tool}</span>
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="pt-8 border-t border-white/5">
                                {isVideo && project.videoUrl && (
                                    <a
                                        href={project.videoUrl}
                                        target="_blank"
                                        className="flex items-center justify-center w-full px-6 py-4 bg-amber-500 text-black font-bold rounded-2xl hover:bg-white transition-all text-sm mb-4"
                                    >
                                        <PlayCircle size={18} className="mr-2" />
                                        Watch Original
                                    </a>
                                )}
                                <button className="flex items-center justify-center w-full px-6 py-4 bg-white/5 border border-white/10 text-white font-bold rounded-2xl hover:bg-white/10 transition-all text-sm">
                                    <ExternalLink size={18} className="mr-2" />
                                    Share Project
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
