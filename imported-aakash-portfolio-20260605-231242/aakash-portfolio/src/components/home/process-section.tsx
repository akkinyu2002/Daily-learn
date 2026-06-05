export default function ProcessSection() {
  const steps = [
    { title: "Discovery", desc: "Understand goals and constraints" },
    { title: "Planning", desc: "Outline milestones and deliverables" },
    { title: "Creation", desc: "Execute edits and designs" },
    { title: "Delivery", desc: "Final handoff and assets" },
  ];

  return (
    <section className="mx-auto max-w-6xl px-6 py-12">
      <h2 className="text-xl font-semibold">My Process</h2>
      <div className="mt-6 grid gap-4 sm:grid-cols-4">
        {steps.map((s, i) => (
          <div key={s.title} className="rounded-lg border p-4 text-center">
            <div className="mx-auto mb-2 h-10 w-10 rounded-full bg-zinc-100 dark:bg-zinc-900 flex items-center justify-center">{i+1}</div>
            <h3 className="font-medium">{s.title}</h3>
            <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">{s.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
