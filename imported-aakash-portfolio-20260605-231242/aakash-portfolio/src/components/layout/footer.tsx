export default function Footer() {
  return (
    <footer className="border-t bg-white dark:bg-black">
      <div className="mx-auto max-w-4xl px-6 py-8 text-sm text-zinc-500 text-center">
        © {new Date().getFullYear()} Aakash Nyupane. All rights reserved.
      </div>
    </footer>
  );
}
