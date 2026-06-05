import { projects } from "../../lib/data/projects";

export default function WorkPage() {
  return (
    <div className="mx-auto max-w-6xl px-6 py-20">
      <h1 className="text-3xl font-bold">All Projects</h1>
      <div className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {projects.map((p) => (
          <article key={p.id} className="rounded-lg border p-4">
            <div className="h-40 w-full rounded bg-zinc-100 dark:bg-zinc-900" />
            <h3 className="mt-3 font-medium">{p.name}</h3>
            <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">{p.description}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
