export default function MetricsSection() {
  const metrics = [
    { label: "Projects", value: "50+" },
    { label: "Videos", value: "100+" },
    { label: "Views", value: "1M+" },
    { label: "Languages", value: "3" },
  ];

  return (
    <section className="mx-auto max-w-6xl px-6 py-12">
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {metrics.map((m) => (
          <div key={m.label} className="rounded-lg border p-4 text-center">
            <div className="text-2xl font-bold">{m.value}</div>
            <div className="mt-1 text-sm text-zinc-600">{m.label}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
