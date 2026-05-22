import React from 'react'
import {
  AlertTriangle, ShieldOff, Film, Tv, Star, Clock, Globe, Sparkles,
  PlayCircle, Bookmark, Download, Smartphone, Laptop, Monitor,
  CheckCircle2, Lock, Users, CreditCard, Languages,
} from 'lucide-react'

const fmtDuration = (mins) => {
  if (!mins) return ''
  const h = Math.floor(mins / 60), m = mins % 60
  return h > 0 ? `${h}h ${m}m` : `${m}m`
}

// ============ Plain text ============
export function TextBlock({ content }) {
  const html = content
    .split(/\n\n/)
    .map((para) => para.replace(/\*\*(.+?)\*\*/g, '<strong class="text-accent-300 font-semibold">$1</strong>'))
    .map((para) => `<p class="mb-2 last:mb-0">${para.replace(/\n/g, '<br/>')}</p>`)
    .join('')
  return <div className="text-slate-200 leading-relaxed" dangerouslySetInnerHTML={{ __html: html }} />
}

// ============ Disclaimer ============
export function DisclaimerBlock({ content }) {
  return (
    <div className="mt-2 text-xs italic text-slate-400 bg-slate-900/40 border border-slate-700/50 rounded-lg p-3">
      {content}
    </div>
  )
}

// ============ Content safety refusal ============
export function ContentSafetyBlock({ block }) {
  return (
    <div className="relative bg-gradient-to-br from-accent-900/40 to-accent-950/60 border-2 border-accent-500/70 rounded-xl p-5 shadow-magenta">
      <div className="absolute -inset-px rounded-xl bg-accent-500/10 animate-stream-pulse pointer-events-none" />
      <div className="relative">
        <div className="flex items-start gap-3 mb-3">
          <div className="p-2 bg-accent-500/20 rounded-lg">
            <ShieldOff className="w-6 h-6 text-accent-300" />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-bold text-accent-200">{block.headline}</h3>
            <p className="text-slate-200 mt-2 leading-relaxed">{block.message}</p>
          </div>
        </div>
        {block.indicators?.length > 0 && (
          <div className="mt-4 pl-2">
            <p className="text-xs uppercase tracking-wider text-accent-300/80 font-semibold mb-2">Why this matters</p>
            <ul className="space-y-1.5">
              {block.indicators.map((ind, i) => (
                <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                  <span className="text-accent-400 mt-1">•</span>
                  <span>{ind}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
        {block.offer && (
          <div className="mt-4 p-3 bg-slate-900/60 border border-accent-700/40 rounded-lg">
            <p className="text-sm text-slate-200"><span className="text-accent-300 font-semibold">→ </span>{block.offer}</p>
          </div>
        )}
      </div>
    </div>
  )
}

// ============ Title card (shared) ============
function TitleCard({ t, compact = false }) {
  return (
    <div className={`bg-slate-900/60 border border-slate-700/60 hover:border-accent-500/50 rounded-lg ${compact ? 'p-3' : 'p-4'} transition-all`}>
      <div className="flex items-start justify-between gap-3 mb-2">
        <div className="flex-1">
          <h4 className={`${compact ? 'text-sm' : 'text-base'} font-semibold text-white`}>{t.title}</h4>
          <p className="text-xs text-slate-400 mt-0.5">
            {t.id} · {t.type === 'series' ? `${t.seasons}S · ${t.episodes_total}E` : t.type === 'documentary' ? 'Documentary' : 'Movie'}
            {t.year && ` · ${t.year}`}
          </p>
        </div>
        {t.available_in_4k && (
          <span className="px-1.5 py-0.5 bg-accent-500/20 border border-accent-500/40 rounded text-[10px] font-bold text-accent-300">4K</span>
        )}
      </div>
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-300 mb-2">
        <span className="flex items-center gap-1"><Star className="w-3 h-3 text-amber-400" />{t.imdb}</span>
        <span className="px-1.5 py-0.5 bg-slate-800 rounded text-[10px] text-slate-400 font-medium">{t.rating}</span>
        <span className="flex items-center gap-1 text-slate-400">
          <Clock className="w-3 h-3" />
          {t.type === 'series' ? `~${t.episode_avg_min}m/ep` : fmtDuration(t.duration_min)}
        </span>
      </div>
      {!compact && (
        <div className="flex flex-wrap gap-1 mt-2">
          {t.genres?.slice(0, 3).map((g) => (
            <span key={g} className="text-[10px] px-1.5 py-0.5 bg-slate-800/80 text-slate-300 rounded">{g}</span>
          ))}
        </div>
      )}
    </div>
  )
}

// ============ Title list ============
export function TitleListBlock({ block }) {
  return (
    <div className="bg-slate-900/40 border border-slate-700/60 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-bold text-accent-200 uppercase tracking-wide">{block.title || 'Results'}</h3>
        <span className="text-xs text-slate-400">{block.total} total · showing {block.items.length}</span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {block.items.map((t) => <TitleCard key={t.id} t={t} />)}
      </div>
    </div>
  )
}

// ============ Title detail ============
export function TitleDetailBlock({ block }) {
  const t = block.title
  return (
    <div className="bg-gradient-to-br from-slate-900/80 to-slate-950/80 border border-accent-500/40 rounded-xl p-5 shadow-magenta">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <p className="text-xs text-accent-400 font-semibold tracking-wider uppercase">
            {t.type === 'series' ? `${t.seasons} Season${t.seasons > 1 ? 's' : ''} · ${t.episodes_total} Episodes` : t.type}
            {t.year && ` · ${t.year}`}
          </p>
          <h3 className="text-2xl font-bold text-white mt-1">{t.title}</h3>
          <p className="text-xs text-slate-500 mt-1">{t.id}</p>
        </div>
        {t.available_in_4k && (
          <span className="px-2 py-1 bg-accent-500/20 border border-accent-500/50 rounded text-xs font-bold text-accent-200">4K · HDR</span>
        )}
      </div>
      <div className="flex flex-wrap items-center gap-3 mb-4 text-sm">
        <span className="flex items-center gap-1.5 text-amber-300"><Star className="w-4 h-4" />{t.imdb}/10</span>
        <span className="px-2 py-0.5 bg-slate-800 border border-slate-700 rounded text-slate-300 text-xs font-medium">{t.rating}</span>
        <span className="flex items-center gap-1.5 text-slate-400 text-xs">
          <Clock className="w-4 h-4" />
          {t.type === 'series' ? `~${t.episode_avg_min}m per ep` : fmtDuration(t.duration_min)}
        </span>
      </div>
      <p className="text-slate-200 leading-relaxed mb-4">{t.synopsis}</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
        <div>
          <p className="text-xs uppercase tracking-wider text-slate-400 mb-1">Cast</p>
          <p className="text-slate-200">{t.cast?.join(', ')}</p>
        </div>
        <div>
          <p className="text-xs uppercase tracking-wider text-slate-400 mb-1">{t.type === 'series' ? 'Showrunner' : 'Director'}</p>
          <p className="text-slate-200">{t.showrunner || t.director}</p>
        </div>
        <div>
          <p className="text-xs uppercase tracking-wider text-slate-400 mb-1 flex items-center gap-1"><Languages className="w-3 h-3" />Audio</p>
          <p className="text-slate-300 text-xs">{t.languages?.join(' · ')}</p>
          <p className="text-slate-500 text-xs mt-1">{t.audio?.join(' / ')}</p>
        </div>
        <div>
          <p className="text-xs uppercase tracking-wider text-slate-400 mb-1">Subtitles</p>
          <p className="text-slate-300 text-xs">{t.subtitles?.join(' · ')}</p>
        </div>
      </div>
      <div className="flex flex-wrap gap-2 mt-4">
        {t.genres?.map((g) => (
          <span key={g} className="text-xs px-2 py-1 bg-accent-500/10 text-accent-200 border border-accent-500/30 rounded">{g}</span>
        ))}
      </div>
    </div>
  )
}

// ============ Trailer ============
export function TrailerBlock({ block }) {
  const mins = Math.floor(block.duration_seconds / 60)
  const secs = block.duration_seconds % 60
  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-accent-700/30 via-accent-900/40 to-slate-950/80 border border-accent-500/40 rounded-xl p-6 shadow-magenta">
      <div className="flex items-center gap-4">
        <div className="flex-shrink-0 p-4 bg-accent-500/30 rounded-full">
          <PlayCircle className="w-12 h-12 text-white" strokeWidth={1.5} />
        </div>
        <div className="flex-1">
          <p className="text-xs text-accent-300 uppercase tracking-wider font-semibold">Trailer</p>
          <h3 className="text-xl font-bold text-white mt-1">{block.title}</h3>
          <p className="text-xs text-slate-400 mt-1">{block.title_id} · {mins}:{String(secs).padStart(2, '0')}</p>
        </div>
      </div>
      <p className="text-xs text-slate-400 italic mt-4">{block.note}</p>
    </div>
  )
}

// ============ Continue watching ============
export function ContinueWatchingBlock({ block }) {
  return (
    <div className="bg-slate-900/40 border border-slate-700/60 rounded-xl p-4">
      <h3 className="text-sm font-bold text-accent-200 uppercase tracking-wide mb-3">Continue Watching</h3>
      <div className="space-y-3">
        {block.items.map((it, i) => {
          const pct = Math.round((it.progress_min / it.total_min) * 100)
          const t = it._title
          return (
            <div key={i} className="bg-slate-900/60 border border-slate-700/60 rounded-lg p-3">
              <div className="flex items-start justify-between gap-3 mb-2">
                <div className="flex-1">
                  <h4 className="text-sm font-semibold text-white">{t?.title}</h4>
                  <p className="text-xs text-slate-400 mt-0.5">
                    {it.season ? `S${it.season} · E${it.episode}` : 'Movie'} · {it.last_watched}
                  </p>
                </div>
                <span className="text-xs text-accent-300 font-medium">{pct}%</span>
              </div>
              <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-accent-500 to-accent-400" style={{ width: `${pct}%` }} />
              </div>
              <p className="text-xs text-slate-500 mt-1.5">{it.progress_min}m of {it.total_min}m</p>
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ============ Watchlist ============
export function WatchlistBlock({ block }) {
  return (
    <div className="bg-slate-900/40 border border-slate-700/60 rounded-xl p-4">
      <h3 className="text-sm font-bold text-accent-200 uppercase tracking-wide mb-3 flex items-center gap-2">
        <Bookmark className="w-4 h-4" />My Watchlist
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {block.items.map((it) => (
          <div key={it.title_id} className="bg-slate-900/60 border border-slate-700/60 rounded-lg p-3">
            <h4 className="text-sm font-semibold text-white">{it._title?.title}</h4>
            <p className="text-xs text-slate-400 mt-0.5">{it._title?.id} · {it._title?.rating}</p>
            <p className="text-xs text-slate-500 mt-1">Added {it.added_on}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

// ============ Downloads ============
export function DownloadsBlock({ block }) {
  return (
    <div className="bg-slate-900/40 border border-slate-700/60 rounded-xl p-4">
      <h3 className="text-sm font-bold text-accent-200 uppercase tracking-wide mb-3 flex items-center gap-2">
        <Download className="w-4 h-4" />Downloads
      </h3>
      <div className="space-y-2">
        {block.items.map((it, i) => (
          <div key={i} className="bg-slate-900/60 border border-slate-700/60 rounded-lg p-3 flex items-center justify-between gap-3">
            <div className="flex-1 min-w-0">
              <h4 className="text-sm font-semibold text-white truncate">{it._title?.title}</h4>
              <p className="text-xs text-slate-400 mt-0.5">
                {it.season ? `S${it.season} E${it.episode}` : 'Movie'} · {it.quality} · {it.size_mb} MB · on {it.device}
              </p>
            </div>
            <span className="text-xs text-amber-300 whitespace-nowrap">expires in {it.expires_in_days}d</span>
          </div>
        ))}
      </div>
    </div>
  )
}

// ============ Recommendation ============
export function RecommendationBlock({ block }) {
  return (
    <div className="bg-gradient-to-br from-accent-900/20 to-slate-900/40 border border-accent-500/30 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <Sparkles className="w-4 h-4 text-accent-400" />
        <h3 className="text-sm font-bold text-accent-200 uppercase tracking-wide">Recommended for you</h3>
      </div>
      <p className="text-xs text-slate-300 mb-3 italic">{block.rationale}</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {block.items.map((t) => <TitleCard key={t.id} t={t} />)}
      </div>
    </div>
  )
}

// ============ Profiles ============
const avatarBg = {
  indigo: 'from-indigo-500 to-indigo-700',
  amber:  'from-amber-500 to-amber-700',
  teal:   'from-teal-500 to-teal-700',
}
export function ProfilesBlock({ block }) {
  return (
    <div className="bg-slate-900/40 border border-slate-700/60 rounded-xl p-4">
      <h3 className="text-sm font-bold text-accent-200 uppercase tracking-wide mb-3 flex items-center gap-2">
        <Users className="w-4 h-4" />Profiles
      </h3>
      <div className="grid grid-cols-3 gap-3">
        {block.items.map((p) => {
          const isActive = p.name === block.active_profile
          return (
            <div key={p.id} className={`text-center p-3 rounded-lg border ${isActive ? 'border-accent-500 bg-accent-500/10' : 'border-slate-700 bg-slate-900/40'}`}>
              <div className={`w-16 h-16 mx-auto rounded-full bg-gradient-to-br ${avatarBg[p.avatar] || 'from-slate-500 to-slate-700'} flex items-center justify-center text-2xl font-bold text-white`}>
                {p.name[0]}
              </div>
              <p className="text-sm font-semibold text-white mt-2">{p.name}</p>
              <div className="flex items-center justify-center gap-1 mt-1">
                <span className={`text-[10px] px-1.5 py-0.5 rounded ${p.type === 'kids' ? 'bg-teal-500/20 text-teal-300' : 'bg-slate-700 text-slate-300'}`}>{p.type}</span>
                {p.pin_protected && <Lock className="w-3 h-3 text-amber-400" />}
              </div>
              {isActive && <p className="text-[10px] text-accent-300 font-semibold mt-1">● Active</p>}
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ============ Plans (3-column comparison) ============
export function PlansBlock({ block }) {
  return (
    <div className="bg-slate-900/40 border border-slate-700/60 rounded-xl p-4">
      <h3 className="text-sm font-bold text-accent-200 uppercase tracking-wide mb-3">Plans</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {block.items.map((p) => {
          const isCurrent = p.id === block.current_plan_id
          return (
            <div key={p.id} className={`p-4 rounded-lg border-2 ${isCurrent ? 'border-accent-500 bg-accent-500/10 shadow-magenta' : 'border-slate-700 bg-slate-900/60'}`}>
              <div className="flex items-start justify-between mb-2">
                <h4 className="text-lg font-bold text-white">{p.name}</h4>
                {isCurrent && <span className="text-[10px] px-1.5 py-0.5 bg-accent-500 text-white rounded font-bold">CURRENT</span>}
              </div>
              <p className="text-2xl font-bold text-accent-200">₹{p.price_inr}<span className="text-xs text-slate-400 font-normal">/{p.billing.slice(0, 2)}</span></p>
              <div className="mt-3 space-y-1.5 text-xs text-slate-300">
                <div className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3 text-accent-400 flex-shrink-0" />{p.max_quality}</div>
                <div className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3 text-accent-400 flex-shrink-0" />{p.audio}</div>
                <div className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3 text-accent-400 flex-shrink-0" />{p.devices}</div>
                <div className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3 text-accent-400 flex-shrink-0" />{p.downloads} downloads</div>
                <div className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3 text-accent-400 flex-shrink-0" />{p.ads}</div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ============ Subscription (current plan) ============
export function SubscriptionBlock({ block }) {
  return (
    <div className="bg-gradient-to-br from-accent-900/30 to-slate-950/80 border border-accent-500/50 rounded-xl p-5">
      <div className="flex items-start justify-between mb-3">
        <div>
          <p className="text-xs text-accent-300 uppercase tracking-wider font-semibold">Your subscription</p>
          <h3 className="text-2xl font-bold text-white mt-1">{block.plan.name}</h3>
        </div>
        <CreditCard className="w-6 h-6 text-accent-400" />
      </div>
      <div className="grid grid-cols-2 gap-3 text-sm">
        <div>
          <p className="text-xs text-slate-400 uppercase">Renews</p>
          <p className="text-slate-200 font-medium">{block.subscription.renews_on}</p>
        </div>
        <div>
          <p className="text-xs text-slate-400 uppercase">Amount</p>
          <p className="text-slate-200 font-medium">₹{block.subscription.amount_inr} / {block.plan.billing}</p>
        </div>
        <div>
          <p className="text-xs text-slate-400 uppercase">Auto-renew</p>
          <p className="text-slate-200 font-medium">{block.subscription.auto_renew ? 'On' : 'Off'}</p>
        </div>
        <div>
          <p className="text-xs text-slate-400 uppercase">Payment</p>
          <p className="text-slate-200 font-medium">{block.subscription.payment_method}</p>
        </div>
      </div>
    </div>
  )
}

// ============ Devices ============
const deviceIcon = { phone: Smartphone, laptop: Laptop, tv: Monitor }
export function DevicesBlock({ block }) {
  return (
    <div className="bg-slate-900/40 border border-slate-700/60 rounded-xl p-4">
      <h3 className="text-sm font-bold text-accent-200 uppercase tracking-wide mb-3">Devices</h3>
      <div className="space-y-2">
        {block.items.map((d) => {
          const Icon = deviceIcon[d.type] || Smartphone
          return (
            <div key={d.id} className="bg-slate-900/60 border border-slate-700/60 rounded-lg p-3 flex items-center gap-3">
              <div className="p-2 bg-slate-800 rounded">
                <Icon className="w-4 h-4 text-accent-400" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-white">{d.name}</p>
                <p className="text-xs text-slate-400">{d.type} · last active {d.last_active}</p>
              </div>
              {d.is_current && <span className="text-[10px] px-1.5 py-0.5 bg-accent-500/20 text-accent-300 rounded font-bold">THIS</span>}
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ============ Parental controls ============
export function ParentalControlsBlock({ block }) {
  const kp = block.kids_profile
  return (
    <div className="bg-gradient-to-br from-teal-900/20 to-slate-900/40 border border-teal-500/30 rounded-xl p-4">
      <h3 className="text-sm font-bold text-teal-200 uppercase tracking-wide mb-3 flex items-center gap-2">
        <Lock className="w-4 h-4" />Parental Controls
      </h3>
      <div className="bg-slate-900/60 border border-slate-700/60 rounded-lg p-3 mb-3 flex items-center gap-3">
        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-teal-500 to-teal-700 flex items-center justify-center font-bold text-white">
          {kp.name[0]}
        </div>
        <div className="flex-1">
          <p className="text-sm font-semibold text-white">{kp.name} Profile</p>
          <p className="text-xs text-slate-400">PIN protected · max rating {kp.max_rating}</p>
        </div>
      </div>
      <div className="mb-3">
        <p className="text-xs uppercase text-slate-400 tracking-wider mb-2">Blocked ratings</p>
        <div className="flex flex-wrap gap-1.5">
          {block.age_ratings_blocked.map((r) => (
            <span key={r} className="text-xs px-2 py-1 bg-red-500/10 text-red-300 border border-red-500/30 rounded">{r}</span>
          ))}
        </div>
      </div>
      <p className="text-xs text-slate-400 italic leading-relaxed">{block.note}</p>
    </div>
  )
}

// ============ Dispatcher ============
export function Block({ block }) {
  switch (block.type) {
    case 'text':                return <TextBlock content={block.content} />
    case 'disclaimer':          return <DisclaimerBlock content={block.content} />
    case 'content_safety':      return <ContentSafetyBlock block={block} />
    case 'title_list':          return <TitleListBlock block={block} />
    case 'title_detail':        return <TitleDetailBlock block={block} />
    case 'trailer':             return <TrailerBlock block={block} />
    case 'continue_watching':   return <ContinueWatchingBlock block={block} />
    case 'watchlist':           return <WatchlistBlock block={block} />
    case 'downloads':           return <DownloadsBlock block={block} />
    case 'recommendation':      return <RecommendationBlock block={block} />
    case 'profiles':            return <ProfilesBlock block={block} />
    case 'plans':               return <PlansBlock block={block} />
    case 'subscription':        return <SubscriptionBlock block={block} />
    case 'devices':             return <DevicesBlock block={block} />
    case 'parental_controls':   return <ParentalControlsBlock block={block} />
    default:
      return <pre className="text-xs text-slate-400">{JSON.stringify(block, null, 2)}</pre>
  }
}
