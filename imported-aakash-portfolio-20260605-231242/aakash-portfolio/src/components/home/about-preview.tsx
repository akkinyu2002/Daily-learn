export default function AboutPreview() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-12">
      <h2 className="text-xl font-semibold">About</h2>
      <div className="mt-4 flex flex-col items-start gap-4 md:flex-row md:items-center">
        <div className="h-32 w-32 rounded-full bg-zinc-100 dark:bg-zinc-900" />
        <div>
          <p className="max-w-xl text-zinc-700 dark:text-zinc-300">I combine video editing, graphic design, and web tools to build polished content and systems.</p>
          <a href="/about" className="mt-3 inline-block text-accent hover:underline">Read full story</a>
        </div>
      </div>
    </section>
  );
}
