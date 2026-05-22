const API_BASE = import.meta.env.DEV ? '/api' : (import.meta.env.VITE_API_BASE || '/api')

export async function sendChat(message, sessionId) {
  const r = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId }),
  })
  if (!r.ok) throw new Error(`HTTP ${r.status}`)
  return r.json()
}
