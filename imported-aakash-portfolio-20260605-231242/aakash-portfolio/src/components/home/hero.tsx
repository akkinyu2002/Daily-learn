export default function Hero() {
  return (
    <section className="mx-auto max-w-4xl px-6 py-24">
      <div className="space-y-6">
        <h1 className="text-5xl font-bold">Aakash Nyupane</h1>
        <p className="text-xl text-zinc-600 dark:text-zinc-300 max-w-2xl leading-relaxed">
          I'm a video editor, graphic designer, and creative technologist. I help creators and businesses with professional editing, design, and web solutions.
        </p>
        <div className="flex gap-3 pt-4">
          <a href="#projects" className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded text-sm font-medium">
            View Projects
          </a>
          <a href="/contact" className="border border-zinc-300 dark:border-zinc-600 px-6 py-2 rounded text-sm font-medium hover:bg-zinc-50 dark:hover:bg-zinc-900">
            Get in touch
          </a>
        </div>
      </div>
    </section>
  );
}
