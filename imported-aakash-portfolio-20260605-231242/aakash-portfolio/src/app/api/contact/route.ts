import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const data = await req.json();
    // Basic validation
    if (!data.email || !data.message) {
      return NextResponse.json({ ok: false, error: 'Missing fields' }, { status: 400 });
    }

    // Placeholder: integrate Resend or other email provider here using env var
    // For now, just return success
    return NextResponse.json({ ok: true });
  } catch (err) {
    return NextResponse.json({ ok: false, error: 'Invalid request' }, { status: 400 });
  }
}
