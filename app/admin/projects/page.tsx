"use client";

import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
    Plus,
    Trash2,
    Edit3,
    ExternalLink,
    Search,
    LayoutGrid,
    List as ListIcon,
    ChevronLeft
} from "lucide-react";
import Link from "next/link";
import ProjectForm from "@/components/admin/ProjectForm";

export default function ProjectsManagementPage() {
    const { data: session, status } = useSession();
    const router = useRouter();
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [showForm, setShowForm] = useState(false);
    const [editingProject, setEditingProject] = useState(null);

    useEffect(() => {
        if (status === "unauthenticated") {
            router.push("/admin/login");
        }

        if (status === "authenticated") {
            fetchProjects();
        }
    }, [status, router]);

    const fetchProjects = async () => {
        setLoading(true);
        try {
            const res = await fetch("/api/projects");
            const data = await res.json();
            setProjects(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const deleteProject = async (id) => {
        if (!confirm("Are you sure you want to delete this project?")) return;

        try {
            const res = await fetch(`/api/projects/${id}`, { method: "DELETE" });
            if (res.ok) {
                setProjects(projects.filter(p => p._id !== id));
            }
        } catch (err) {
            console.error(err);
        }
    };

    const openAddForm = () => {
        setEditingProject(null);
        setShowForm(true);
    };

    const openEditForm = (project) => {
        setEditingProject(project);
        setShowForm(true);
    };

    if (status === "loading") return null;

    const filteredProjects = projects.filter(p =>
        p.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.category.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="min-h-screen bg-[#0a0a0a] pt-24 pb-12">
            <div className="container mx-auto px-6">
                <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-6">
                    <div className="flex items-center gap-4">
                        <Link href="/admin/dashboard" className="p-2 hover:bg-white/5 rounded-full transition-colors text-white">
                            <ChevronLeft size={24} />
                        </Link>
                        <div>
                            <h1 className="text-3xl font-bold font-space">Manage Projects</h1>
                            <p className="text-gray-500 text-sm">Create, edit, and organize your work</p>
                        </div>
                    </div>

                    <button
                        onClick={openAddForm}
                        className="flex items-center px-6 py-3 bg-white text-black font-bold rounded-full hover:bg-amber-500 transition-all text-sm"
                    >
                        <Plus size={18} className="mr-2" />
                        Add New Project
                    </button>
                </header>

                {/* Search and Filters */}
                <div className="mb-12 flex flex-col md:flex-row gap-4">
                    <div className="relative flex-grow">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
                        <input
                            type="text"
                            placeholder="Search projects..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="w-full bg-white/5 border border-white/5 rounded-2xl pl-12 pr-6 py-4 focus:outline-none focus:border-amber-500 transition-all"
                        />
                    </div>
                </div>

                {/* Projects List */}
                <div className="glass-card rounded-3xl overflow-hidden border-white/5">
                    <table className="w-full text-left">
                        <thead className="bg-white/5 border-b border-white/5">
                            <tr>
                                <th className="px-8 py-6 text-xs uppercase tracking-widest font-bold text-gray-500">Project</th>
                                <th className="px-8 py-6 text-xs uppercase tracking-widest font-bold text-gray-500">Category</th>
                                <th className="px-8 py-6 text-xs uppercase tracking-widest font-bold text-gray-500">Date</th>
                                <th className="px-8 py-6 text-xs uppercase tracking-widest font-bold text-gray-500 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/5">
                            {loading ? (
                                Array(5).fill(0).map((_, i) => (
                                    <tr key={i} className="animate-pulse">
                                        <td colSpan={4} className="px-8 py-6">
                                            <div className="h-4 bg-white/5 rounded w-1/2" />
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                filteredProjects.map((project) => (
                                    <tr key={project._id} className="hover:bg-white/5 transition-colors group">
                                        <td className="px-8 py-6">
                                            <div className="flex items-center gap-4">
                                                <div className="w-12 h-12 rounded-lg bg-gray-900 overflow-hidden border border-white/10">
                                                    {/* eslint-disable-next-line @next/next/no-img-element */}
                                                    <img src={project.thumbnail} alt="" className="w-full h-full object-cover" />
                                                </div>
                                                <div>
                                                    <h4 className="font-bold text-white text-sm">{project.title}</h4>
                                                    <Link
                                                        href={`/portfolio/${project._id}`}
                                                        target="_blank"
                                                        className="text-[10px] text-gray-500 hover:text-amber-500 flex items-center mt-1"
                                                    >
                                                        View Public <ExternalLink size={10} className="ml-1" />
                                                    </Link>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-8 py-6">
                                            <span className="px-3 py-1 bg-white/5 rounded-full text-[10px] font-bold text-gray-400">
                                                {project.category}
                                            </span>
                                        </td>
                                        <td className="px-8 py-6 text-sm text-gray-500">
                                            {new Date(project.createdAt).toLocaleDateString()}
                                        </td>
                                        <td className="px-8 py-6 text-right">
                                            <div className="flex items-center justify-end gap-2">
                                                <button
                                                    onClick={() => openEditForm(project)}
                                                    className="p-2 hover:bg-amber-500 hover:text-black rounded-lg transition-all text-gray-500"
                                                >
                                                    <Edit3 size={18} />
                                                </button>
                                                <button
                                                    onClick={() => deleteProject(project._id)}
                                                    className="p-2 hover:bg-red-500 hover:text-white rounded-lg transition-all text-gray-500"
                                                >
                                                    <Trash2 size={18} />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>

                    {!loading && filteredProjects.length === 0 && (
                        <div className="py-24 text-center">
                            <p className="text-gray-500">No projects found.</p>
                        </div>
                    )}
                </div>

                {/* Modal Form */}
                <AnimatePresence>
                    {showForm && (
                        <ProjectForm
                            project={editingProject}
                            onClose={() => setShowForm(false)}
                            onSave={fetchProjects}
                        />
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
