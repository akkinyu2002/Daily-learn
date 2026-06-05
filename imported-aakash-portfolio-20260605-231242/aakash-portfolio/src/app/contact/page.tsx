"use client";

import { useState } from "react";

export default function ContactPage() {
  const [status, setStatus] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = new FormData(e.currentTarget as HTMLFormElement);
    const body = Object.fromEntries(form as any);
    setStatus("sending");
    try {
      const res = await fetch('/api/contact', { method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json' } });
      if (res.ok) setStatus('sent');
      else setStatus('error');
    } catch (err) {
      setStatus('error');
    }
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-20">
      <h1 className="text-3xl font-bold">Contact</h1>
      <form className="mt-6 grid gap-4" onSubmit={onSubmit}>
        <input name="name" placeholder="Name" className="rounded border px-3 py-2" required />
        <input name="email" type="email" placeholder="Email" className="rounded border px-3 py-2" required />
        <select name="type" className="rounded border px-3 py-2">
          <option>Project</option>
          <option>Collab</option>
          <option>Other</option>
        </select>
        <textarea name="message" placeholder="Message" className="rounded border px-3 py-2" rows={6} />
        <div>
          <button type="submit" className="rounded-full bg-accent px-4 py-2 text-white">Send</button>
        </div>
        {status === 'sending' && <div>Sending…</div>}
        {status === 'sent' && <div>Thanks! Message sent.</div>}
        {status === 'error' && <div>Something went wrong.</div>}
      </form>
    </div>
  );
}
