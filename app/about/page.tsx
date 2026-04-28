import { motion } from "framer-motion";

export default function AboutPage() {
    const skills = ["Premiere Pro", "After Effects", "Photoshop", "Illustrator", "Next.js", "Tailwind CSS"];

    return (
        <div className="pt-32 pb-24 min-h-screen">
            <div className="container mx-auto px-6">
                <div className="flex flex-col md:flex-row gap-16 items-center">
                    {/* Image placeholder */}
                    <div className="w-full md:w-1/2">
                        <div className="relative aspect-[4/5] rounded-3xl overflow-hidden glass-card group">
                            {/* Replace with real image later */}
                            <div className="absolute inset-0 bg-gradient-to-tr from-amber-500/20 to-blue-500/20" />
                            <div className="absolute bottom-10 left-10 p-8 glass-card rounded-2xl">
                                <h3 className="text-2xl font-bold font-space">Akash Neupane</h3>
                                <p className="text-amber-500 text-sm font-semibold tracking-wider">CREATIVE MIND</p>
                            </div>
                        </div>
                    </div>

                    <div className="w-full md:w-1/2">
                        <h1 className="text-4xl md:text-6xl font-bold font-space tracking-tighter mb-8 italic">
                            The Story <span className="text-amber-500">So Far</span>
                        </h1>

                        <div className="space-y-6 text-gray-400 leading-relaxed text-lg">
                            <p>
                                I am a dedicated professional with a background in IT and a Diploma in Computer Engineering. My journey is fueled by a passion for visual storytelling and innovative digital media.
                            </p>
                            <p>
                                With hands-on experience in graphic design, front-end development, and video editing, I've had the privilege of working with organizations like Saraswati Secondary School and Saraswati Secondary School during my OJT.
                            </p>
                        </div>

                        <div className="mt-12">
                            <h3 className="text-xl font-bold font-space mb-6 flex items-center">
                                Skills & Tools <div className="ml-4 h-px flex-grow bg-white/10" />
                            </h3>
                            <div className="flex flex-wrap gap-3">
                                {skills.map(skill => (
                                    <span key={skill} className="px-5 py-2 rounded-xl bg-white/5 border border-white/5 text-sm hover:border-amber-500/50 transition-colors">
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        </div>

                        <div className="mt-12 p-8 glass-card rounded-3xl">
                            <div className="flex items-center space-x-4 mb-4">
                                <div className="w-10 h-10 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-500 font-bold">
                                    !
                                </div>
                                <h4 className="font-bold font-space text-white">Experience Focus</h4>
                            </div>
                            <p className="text-sm text-gray-500 leading-relaxed">
                                Specializing in commercial video editing, brand identity systems, and high-engagement social media content for startups and individual creators.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
