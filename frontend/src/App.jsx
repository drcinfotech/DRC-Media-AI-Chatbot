import React, { useState, useRef, useEffect } from 'react'
import { Film, Send, Loader2 } from 'lucide-react'
import { sendChat } from './api'
import { Block } from './components/Blocks.jsx'

const INITIAL_SUGGESTIONS = [
  'Recommend something',
  'Continue watching',
  'My watchlist',
  'Browse plans',
]

function MessageBubble({ message, blocks, suggestions, onSuggestion, safetyFlag }) {
  const isUser = message.role === 'user'
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex gap-3 max-w-3xl ${isUser ? 'flex-row-reverse' : ''}`}>
        {!isUser && (
          <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-accent-500 to-accent-700 flex items-center justify-center shadow-magenta">
            <Film className="w-5 h-5 text-white" />
          </div>
        )}
        <div className={`flex-1 ${isUser ? 'text-right' : ''}`}>
          {isUser ? (
            <div className="inline-block bg-accent-500/20 border border-accent-500/40 rounded-2xl rounded-tr-sm px-4 py-2 text-slate-100">
              {message.text}
            </div>
          ) : (
            <div className="space-y-3">
              {blocks?.map((b, i) => (
                <div key={i}>
                  <Block block={b} />
                </div>
              ))}
              {suggestions?.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-3">
                  {suggestions.map((s, i) => (
                    <button
                      key={i}
                      onClick={() => onSuggestion(s)}
                      className="text-xs px-3 py-1.5 bg-accent-500/10 hover:bg-accent-500/20 border border-accent-500/30 hover:border-accent-500/60 rounded-full text-accent-200 transition-all"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      blocks: [
        { type: 'text',
          content: 'Hi 👋 — I\'m your **Stream Assistant**. I can help you find titles, resume what you were watching, build a watchlist, manage downloads, and tune subscription, profile, and parental-control settings. What sounds good?' }
      ],
      suggestions: INITIAL_SUGGESTIONS,
    },
  ])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const scrollRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, loading])

  async function send(text) {
    const t = text.trim()
    if (!t || loading) return
    setMessages((m) => [...m, { role: 'user', text: t }])
    setInput('')
    setLoading(true)
    try {
      const res = await sendChat(t, sessionId)
      if (res.session_id) setSessionId(res.session_id)
      setMessages((m) => [...m, {
        role: 'assistant',
        blocks: res.blocks,
        suggestions: res.suggestions,
        safetyFlag: res.safety_flag,
      }])
    } catch (e) {
      setMessages((m) => [...m, {
        role: 'assistant',
        blocks: [{ type: 'text', content: `Something went wrong — ${e.message}. Make sure the backend is running on :8000.` }],
      }])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="hidden md:flex w-72 flex-col border-r border-slate-800/60 bg-slate-950/60 backdrop-blur p-5">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-accent-500 to-accent-700 flex items-center justify-center shadow-magenta">
            <Film className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white leading-tight">Stream Assistant</h1>
            <p className="text-[10px] text-accent-300 uppercase tracking-widest">Media · Entertainment · Content</p>
          </div>
        </div>

        <div className="mb-5">
          <h2 className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2">What I can help with</h2>
          <ul className="space-y-1.5 text-sm text-slate-300">
            <li>• Find titles by genre or language</li>
            <li>• Recommendations for tonight</li>
            <li>• Continue watching & watchlist</li>
            <li>• Downloads for offline viewing</li>
            <li>• Subscription, profiles, devices</li>
            <li>• Parental controls & ratings</li>
          </ul>
        </div>

        <div className="mb-5">
          <h2 className="text-xs uppercase tracking-wider text-accent-400 font-semibold mb-2">Content safety & honesty</h2>
          <ul className="space-y-1.5 text-sm text-slate-300">
            <li>• Won't help with piracy or DRM bypass</li>
            <li>• Won't impersonate real public figures</li>
            <li>• Refuses confident news verdicts</li>
            <li>• Won't reproduce full copyrighted text</li>
            <li>• Respects parental controls and rating caps</li>
          </ul>
        </div>

        <div className="mt-auto pt-4 border-t border-slate-800/60 text-[10px] text-slate-500 leading-relaxed">
          Demo only. Not a real streaming service. All titles, studios, and pricing are fictional.
        </div>
      </aside>

      {/* Main chat */}
      <main className="flex-1 flex flex-col min-h-screen">
        <header className="md:hidden flex items-center gap-3 px-4 py-3 border-b border-slate-800/60 bg-slate-950/80 backdrop-blur">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-accent-500 to-accent-700 flex items-center justify-center">
            <Film className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-sm font-bold text-white">Stream Assistant</h1>
            <p className="text-[10px] text-accent-300 uppercase tracking-widest">Media AI Chatbot</p>
          </div>
        </header>

        <div className="hidden md:block px-8 py-5 border-b border-slate-800/60">
          <h2 className="text-xl font-bold text-white">Stream Assistant</h2>
          <p className="text-sm text-slate-400 mt-0.5">Find your next favorite.</p>
        </div>

        <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 md:px-8 py-6">
          <div className="max-w-4xl mx-auto">
            {messages.map((m, i) => (
              <MessageBubble
                key={i}
                message={m}
                blocks={m.blocks}
                suggestions={m.suggestions}
                onSuggestion={send}
                safetyFlag={m.safetyFlag}
              />
            ))}
            {loading && (
              <div className="flex justify-start mb-4">
                <div className="flex gap-3 max-w-3xl">
                  <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-accent-500 to-accent-700 flex items-center justify-center">
                    <Loader2 className="w-5 h-5 text-white animate-spin" />
                  </div>
                  <div className="flex items-center text-sm text-slate-400 italic">Thinking…</div>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="border-t border-slate-800/60 bg-slate-950/80 backdrop-blur px-4 md:px-8 py-4">
          <div className="max-w-4xl mx-auto">
            <div className="flex gap-2">
              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && send(input)}
                placeholder="Find a movie, recommend something, manage subscription…"
                className="flex-1 bg-slate-900/80 border border-slate-700/60 focus:border-accent-500 focus:ring-2 focus:ring-accent-500/20 rounded-xl px-4 py-3 text-slate-100 placeholder:text-slate-500 outline-none transition-all"
                disabled={loading}
              />
              <button
                onClick={() => send(input)}
                disabled={loading || !input.trim()}
                className="px-4 py-3 bg-gradient-to-br from-accent-500 to-accent-700 hover:from-accent-400 hover:to-accent-600 disabled:opacity-40 disabled:cursor-not-allowed rounded-xl shadow-magenta transition-all"
              >
                <Send className="w-5 h-5 text-white" />
              </button>
            </div>
            <p className="text-[10px] text-slate-500 mt-2 text-center">Demo only · No real streaming service · All titles fictional</p>
          </div>
        </div>
      </main>
    </div>
  )
}
