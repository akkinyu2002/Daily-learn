import Link from 'next/link';

export default function Navbar() {
  return (
    <header className="border-b">
      <nav className="mx-auto max-w-4xl px-6 py-4 flex items-center justify-between">
        <Link href="/" className="font-bold text-lg">Aakash</Link>
        
        <div className="flex items-center gap-4 text-sm">
          <Link href="/work">Projects</Link>
          <Link href="/about">About</Link>
          <Link href="/contact" className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700">Contact</Link>
        </div>
      </nav>
    </header>
  );
}
