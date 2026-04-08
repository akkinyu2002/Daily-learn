"use client";

import { useForm } from "react-hook-form";
import { useState } from "react";
import { X, Upload, Plus, Trash } from "lucide-react";

export default function ProjectForm({ project, onClose, onSave }) {
    const [loading, setLoading] = useState(false);
    const [mediaUrls, setMediaUrls] = useState(project?.mediaUrls || []);
    const [tools, setTools] = useState(project?.toolsUsed || []);
    const [newTool, setNewTool] = useState("");

    const { register, handleSubmit } = useForm({
        defaultValues: project || {
            category: "Video Editing",
            isFeatured: false
        }
    });

    const onSubmit = async (data) => {
        setLoading(true);
        data.mediaUrls = mediaUrls;
        data.toolsUsed = tools;

        try {
            const url = project ? `/api/projects/${project._id}` : "/api/projects";
            const method = project ? "PUT" : "POST";

            const res = await fetch(url, {
                method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });

            if (res.ok) {
                onSave();
                onClose();
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const addTool = () => {
        if (newTool && !tools.includes(newTool)) {
            setTools([...tools, newTool]);
            setNewTool("");
        }
    };

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-black/80 backdrop-blur-sm">
            <div className="w-full max-w-4xl bg-[#0f0f0f] border border-white/10 rounded-3xl overflow-hidden shadow-2xl">
                <div className="flex justify-between items-center p-8 border-b border-white/5">
                    <h2 className="text-2xl font-bold font-space">
                        {project ? "Edit Project" : "New Project"}
                    </h2>
                    <button onClick={onClose} className="p-2 hover:bg-white/5 rounded-full">
                        <X size={24} />
                    </button>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className="p-8 overflow-y-auto max-h-[70vh]">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div className="space-y-6">
                            <div className="space-y-2">
                                <label className="text-xs uppercase tracking-widest font-bold text-gray-500">Title</label>
                                <input {...register("title")} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-amber-500 transition-all font-inter" required />
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs uppercase tracking-widest font-bold text-gray-500">Category</label>
                                <select {...register("category")} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-amber-500 transition-all font-inter">
                                    <option value="Video Editing">Video Editing</option>
                                    <option value="Graphic Design">Graphic Design</option>
                                    <option value="Motion Graphics">Motion Graphics</option>
                                    <option value="Social Media">Social Media</option>
                                </select>
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs uppercase tracking-widest font-bold text-gray-500">Description</label>
                                <textarea {...register("description")} rows={4} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-amber-500 transition-all font-inter" required />
                            </div>
                        </div>

                        <div className="space-y-6">
                            <div className="space-y-2">
                                <label className="text-xs uppercase tracking-widest font-bold text-gray-500">Thumbnail URL</label>
                                <input {...register("thumbnail")} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-amber-500 transition-all font-inter" />
                            </div>

                            <div className="space-y-2">
                                <label className="text-xs uppercase tracking-widest font-bold text-gray-500">Video URL (YouTube/Vimeo)</label>
                                <input {...register("videoUrl")} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-amber-500 transition-all font-inter" />
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <label className="text-xs uppercase tracking-widest font-bold text-gray-500">Client</label>
                                    <input {...register("client")} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-amber-500 transition-all font-inter" />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs uppercase tracking-widest font-bold text-gray-500">Duration</label>
                                    <input {...register("duration")} className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-amber-500 transition-all font-inter" />
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="mt-8 pt-8 border-t border-white/5">
                        <div className="space-y-2 mb-4">
                            <label className="text-xs uppercase tracking-widest font-bold text-gray-500">Tools Used</label>
                            <div className="flex gap-2">
                                <input
                                    value={newTool}
                                    onChange={(e) => setNewTool(e.target.value)}
                                    className="flex-grow bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:border-amber-500 transition-all"
                                    placeholder="e.g. Adobe Premiere Pro"
                                    onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addTool())}
                                />
                                <button type="button" onClick={addTool} className="p-3 bg-amber-500 text-black rounded-xl hover:bg-white transition-all">
                                    <Plus size={20} />
                                </button>
                            </div>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {tools.map(tool => (
                                    <span key={tool} className="flex items-center gap-2 px-3 py-1 bg-white/5 rounded-lg text-xs">
                                        {tool}
                                        <button type="button" onClick={() => setTools(tools.filter(t => t !== tool))} className="text-gray-500 hover:text-red-500">
                                            <X size={12} />
                                        </button>
                                    </span>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="flex justify-end gap-4 mt-8">
                        <button type="button" onClick={onClose} className="px-8 py-3 bg-white/5 rounded-full text-sm font-bold">Cancel</button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="px-8 py-3 bg-amber-500 text-black rounded-full text-sm font-bold hover:bg-white transition-all disabled:opacity-50"
                        >
                            {loading ? "Saving..." : "Save Project"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
