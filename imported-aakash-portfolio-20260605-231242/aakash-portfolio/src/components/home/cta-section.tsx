export default function CtaSection() {
  return (
    <section className="mx-auto max-w-4xl px-6 py-16 border-t text-center">
      <h2 className="text-3xl font-bold">Ready to work together?</h2>
      <p className="mt-3 text-zinc-600 dark:text-zinc-400">Drop me a message and let's create something great.</p>
      <a href="/contact" className="inline-block mt-6 bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded font-medium">
        Contact me
      </a>
    </section>
  );
}
