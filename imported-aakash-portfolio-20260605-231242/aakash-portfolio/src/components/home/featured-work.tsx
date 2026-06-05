import { projects } from "../../lib/data/projects";

export default function FeaturedWork() {
  return (
    <section id="projects" className="mx-auto max-w-4xl px-6 py-16 border-t">
      <h2 className="text-3xl font-bold mb-8">Recent Projects</h2>
      <div className="grid gap-6 md:grid-cols-2">
        {projects.slice(0, 4).map((p) => (
          <div key={p.id} className="border rounded-lg overflow-hidden hover:shadow-md transition">
            <div className="h-32 bg-gradient-to-br from-zinc-200 to-zinc-300 dark:from-zinc-800 dark:to-zinc-900" />
            <div className="p-4">
              <h3 className="font-semibold text-lg">{p.name}</h3>
              <p className="text-sm text-zinc-600 dark:text-zinc-400 mt-2">{p.description}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
