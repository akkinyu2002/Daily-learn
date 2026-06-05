export default function ToolsSection() {
  const tools = ["CapCut", "Premiere", "After Effects", "Photoshop", "Illustrator", "Figma", "Notion"];

  return (
    <section className="mx-auto max-w-6xl px-6 py-12">
      <h2 className="text-xl font-semibold">Tools I Work With</h2>
      <div className="mt-4 grid grid-cols-3 gap-4 sm:grid-cols-4 md:grid-cols-8">
        {tools.map((t) => (
          <div key={t} className="flex items-center justify-center rounded border p-3 text-sm">
            {t}
          </div>
        ))}
      </div>
    </section>
  );
}
