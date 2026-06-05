export default function ServicesPreview() {
  const services = [
    { title: "Video Editing", desc: "Short-form and long-form editing" },
    { title: "Graphic Design", desc: "Thumbnails, posters, social visuals" },
    { title: "AI Content Systems", desc: "Automations and templates" },
  ];

  return (
    <section className="mx-auto max-w-6xl px-6 py-12">
      <h2 className="text-xl font-semibold">Services</h2>
      <div className="mt-6 grid gap-6 sm:grid-cols-3">
        {services.map((s) => (
          <div key={s.title} className="rounded-lg border p-4">
            <h3 className="font-medium">{s.title}</h3>
            <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">{s.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
