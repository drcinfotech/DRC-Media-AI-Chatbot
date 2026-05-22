"""Safety layer for the Media AI Chatbot."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class SafetyResult:
    flag: Optional[Literal[
        "piracy", "deepfake", "news_verification",
        "copyrighted_full", "payment_privacy", "social_engineering",
    ]] = None
    reason: str = ""


PIRACY_PATTERNS = [
    r"\b(where|how)\s+(can\s+i|to)\s+(watch|stream|download)\s+(.{0,40}?)\s*(for\s+free|illegally|without\s+(paying|subscription|account))\b",
    r"\b(free|illegal|cracked|pirated|leaked)\s+(stream|streaming|download|link|copy|version|rip|cam[\s-]?rip)\b",
    r"\b(torrent|magnet|telegram\s+link|reddit\s+link)\s+(for|of|to)\s+\w+",
    r"\b(123movies|fmovies|putlocker|tamilrockers|filmywap|movies123|9xmovies|hdrezka|rarbg|piratebay|thepiratebay|1337x|moviesda)\b",
    r"\bskip\s+(paywall|subscription|paying)\b",
    r"\b(crack|bypass|hack)\s+(drm|widevine)\b",
    r"\b(screen\s*record|screen\s*capture|rip)\s+(this|the)\s+(movie|episode|show|stream)\b",
    r"\bhow\s+to\s+download\s+(this|the)\s+(movie|episode|series|show)\s+(without\s+|to\s+)?(subscription|sub|paying|pay)",
]

DEEPFAKE_PATTERNS = [
    r"\b(write|generate|create|make)\s+(a\s+)?(script|dialogue|monologue|speech|quote|tweet|post)\s+(.{0,40}?)(as|impersonating|in\s+the\s+voice\s+of|pretending\s+to\s+be)\s+(?:[A-Z][a-z]+\s+[A-Z][a-z]+|a\s+real\s+person|a\s+celebrity|a\s+politician)",
    r"\b(deepfake|deep\s*fake|face[\s-]?swap|voice[\s-]?clone|voice[\s-]?clon(?:e|ing))\s+(of|for|video|audio|content)?\b",
    r"\b(make|create)\s+(it\s+)?(look|sound)\s+like\s+(?:[A-Z][a-z]+\s+[A-Z][a-z]+|.{0,30}?(celebrity|politician|actor|actress|prime\s+minister|president))\s+(said|did|posted)",
    r"\bimpersonate\s+(an?\s+)?(real|actual|famous|named)\s+(person|celebrity|actor|actress|politician|public\s+figure)\b",
    r"\b(fake|fabricated|forged)\s+(quote|tweet|statement|video|audio|interview)\s+(from|by|of)\s+(?:[A-Z][a-z]+|a\s+celebrity)",
]

NEWS_VERIFICATION_PATTERNS = [
    r"\bis\s+(this|that|the)\s+(news|story|article|headline|tweet|post)\s+(true|real|fake|accurate|legit|credible|fact)\b",
    r"\b(can\s+you|do\s+you)\s+(verify|fact[\s-]?check|confirm)\s+(this|that|the)\s+(news|claim|story|article|tweet|video)\b",
    r"\bis\s+\w+\s+(news|article|report|story)\s+(real|fake|true|false|misinformation|propaganda)\b",
    r"\bdid\s+(.{0,40}?)\s+(really|actually)\s+(say|do|post|tweet)\s+(this|that)\b",
    r"\bis\s+this\s+(video|photo|image|clip)\s+(real|fake|authentic|deepfake|edited)\b",
]

COPYRIGHTED_FULL_PATTERNS = [
    r"\b(give|send|share|write\s+out|print)\s+(me\s+)?(the\s+)?(full|complete|entire|whole)\s+(lyrics|script|screenplay|chapter|book|episode\s+transcript)\b",
    r"\b(transcribe|write\s+out)\s+(the\s+)?(whole|full|entire)\s+(episode|movie|song|book)\b",
    r"\bfull\s+screenplay\s+(of|for)\s+\w+",
    r"\b(chapter\s+\d+|first\s+chapter|last\s+chapter|whole\s+chapter)\s+(of|from)\s+(['\"]\w|the\s+book)",
]

PAYMENT_PRIVACY_PATTERNS = [
    r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
    r"\bcvv\s+(is|number|code|value)\s+(\w+\s+)?\d{3,4}\b",
    r"\bcvv\s+code\s+is\s+\d{3,4}\b",
    r"\bmy\s+cvv\s+is\s+\d{3,4}\b",
    r"\b(my|the|save|store)\s+(card|credit\s+card|debit\s+card)\s+(number|details?|info)\s+is\b",
    r"\b(remember|memorize|store|save)\s+my\s+(card|cvv|pin|password|otp)",
    r"\bbypass\s+(payment|otp|cvv|verification|3d\s*secure)",
    r"\bskip\s+(payment|otp|verification|2fa|3d\s*secure)",
]

SOCIAL_ENGINEERING_PATTERNS = [
    r"\b(ignore|disregard|forget)\s+(\w+\s+){0,4}(instructions|rules|guidelines|system\s+prompt|safety)",
    r"\byou\s+are\s+now\s+(in\s+|an?\s+)?(admin|administrator|dev|developer|debug|root|owner|content\s+moderator)\s+(mode|user)?",
    r"\bpretend\s+(you\s+are|to\s+be)\s+(an?\s+)?(admin|root|developer|streaming\s+platform\s+staff|content\s+moderator\s+with\s+full\s+access)",
    r"\b(give|provide|reveal|show|tell)\s+(me\s+)?(your\s+)?(system\s+prompt|instructions|api\s+key|source\s+code)",
    r"\benable\s+(developer|admin|debug|root)\s+mode\b",
    r"\bjailbreak\b",
    r"\bDAN\s+mode\b",
    r"\bact\s+as\s+(if\s+)?(you\s+have\s+)?no\s+(rules|restrictions|guidelines|safety|content\s+filter)",
    r"\b(give\s+me\s+)?(free|complimentary)\s+(premium|subscription|account|upgrade|year)\s+(for\s+me\s+)?(please\s+)?(now)?\b",
    r"\bbypass\s+(parental|kids?|child)\s+(controls?|pin|filter|lock)\b",
    r"\bunlock\s+(parental|kids?\s+profile|adult\s+content\s+for\s+kids)\b",
    r"\b(show|let|allow)\s+kids?\s+(profile\s+)?(see|watch|access)\s+(adult|mature|18\+|a\s+rated|a-rated)\b",
    r"\bshow\s+kids?\s+profile\s+adult\s+content\b",
]


def check_safety(text: str) -> SafetyResult:
    t = text.lower()
    for pat in SOCIAL_ENGINEERING_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="social_engineering", reason=pat)
    for pat in PAYMENT_PRIVACY_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="payment_privacy", reason=pat)
    for pat in PIRACY_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="piracy", reason=pat)
    for pat in DEEPFAKE_PATTERNS:
        if re.search(pat, text):
            return SafetyResult(flag="deepfake", reason=pat)
    for pat in NEWS_VERIFICATION_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="news_verification", reason=pat)
    for pat in COPYRIGHTED_FULL_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="copyrighted_full", reason=pat)
    return SafetyResult(flag=None)


def build_piracy_block() -> dict:
    return {
        "type": "content_safety",
        "headline": "I can't help with piracy.",
        "message": "Pirated streams, leaked rips, torrents, and 'free' versions of paid content are illegal almost everywhere, harm the people who made the work, and often come with malware. I won't point you at those sites, share links, or help bypass DRM or paywalls.",
        "indicators": [
            "Pirated sites and torrent indexes are usually riddled with malware and tracking",
            "Indian IT Rules 2021 + Copyright Act 1957 cover online piracy",
            "Creators, dubbing artists, editors, and crew get paid from legitimate streams",
            "Legitimate platforms offer free trials, student plans, and ad-supported tiers",
        ],
        "offer": "What I CAN do: find the title on this platform, point you at the closest legal alternative, suggest similar titles, or check if it's included in any plan with a free trial.",
    }


def build_deepfake_block() -> dict:
    return {
        "type": "content_safety",
        "headline": "I can't impersonate real people.",
        "message": "Scripts, dialogue, quotes, tweets, or audio meant to imitate a specific real person - celebrity, politician, actor, journalist, anyone - cross into deepfake / impersonation territory even if labeled as fiction. They can mislead audiences, harm reputations, and run afoul of personality-rights and defamation law in most jurisdictions.",
        "indicators": [
            "Indian courts have recognized personality rights for actors and public figures",
            "Voice cloning and face-swap content of real people is increasingly regulated",
            "Even 'satire' framing doesn't always protect against defamation claims",
            "Misattributed quotes spread fast and are extremely hard to retract",
        ],
        "offer": "What I CAN do: write dialogue for fictional characters, parody an obvious archetype (without naming a real person), or help you write a critical essay about a real person's actual public statements - sourced and attributed.",
    }


def build_news_verification_block() -> dict:
    return {
        "type": "content_safety",
        "headline": "I'm not a fact-checker.",
        "message": "Confirming whether a specific news story, video, or claim is true or fake takes investigative skills, source verification, and current information I don't have reliable access to. Getting it wrong on a news verification is the kind of mistake that spreads misinformation, so I won't issue a confident verdict either way.",
        "indicators": [
            "India: PIB Fact Check, Alt News, BOOM, Vishvas News, Fact Crescendo",
            "International: Snopes, PolitiFact, Reuters Fact Check, AFP, AP Fact Check",
            "Original-source verification (court records, official statements) beats AI verdicts",
            "Reverse image search (TinEye, Google Images) helps with photo authenticity",
        ],
        "offer": "What I CAN do: help you find the original source of a claim, explain what makes a source credible, or recommend documentaries / journalism on a topic from this platform's catalog.",
    }


def build_copyrighted_full_block() -> dict:
    return {
        "type": "content_safety",
        "headline": "I can't reproduce full copyrighted text.",
        "message": "Full song lyrics, complete screenplays, entire book chapters, or full episode transcripts are copyrighted works. Reproducing them in chat - even briefly - infringes on the creators' rights. I won't print them, even in pieces that add up to the whole.",
        "indicators": [
            "Lyrics: most are licensed through MLC, ASCAP, BMI, IPRS (India) - not free to reproduce",
            "Screenplays: protected as literary works under copyright",
            "Short, transformative quotes for review/analysis may fall under fair use - full reproduction does not",
            "Music-lyrics sites are licensed; chatbots reproducing lyrics are not",
        ],
        "offer": "What I CAN do: discuss themes, give a short cited quote with attribution, summarize a plot, or help you find the licensed source for the work you're after.",
    }


def build_payment_privacy_block() -> dict:
    return {
        "type": "content_safety",
        "headline": "Don't share card details in chat.",
        "message": "I can't accept or store full card numbers, CVV, OTP, or PIN through chat - that's a security risk regardless of who's asking. Real subscription payments go through encrypted PCI-DSS gateways with explicit consent, not free-text chat.",
        "indicators": [
            "Card details typed in chat may be logged in plaintext",
            "Legitimate payment flows always use a dedicated, encrypted UI",
            "OTPs and PINs should NEVER be shared with anyone - including chatbots",
            "Streaming subscription scams often start with 'just confirm your card to renew'",
        ],
        "offer": "When you're ready to update payment, the subscription settings handle cards / UPI / wallets through a proper gateway. Ask me to walk you to billing settings and I will.",
    }


def build_social_engineering_block() -> dict:
    return {
        "type": "content_safety",
        "headline": "I can't do that.",
        "message": "I won't bypass my safety rules, switch into 'admin' mode, hand out free premium subscriptions, unlock kids profile beyond its rating cap, reveal internal instructions, or disable the content filter. If you have a real streaming question, I'm happy to help with that.",
        "indicators": [
            "I work the same way for everyone - there's no privileged mode",
            "Parental controls protect children; bypassing them isn't a feature, it's a vulnerability",
            "Real subscription support can do things I can't (refunds, plan changes)",
            "Use 'Contact support' for anything beyond search and recommendations",
        ],
        "offer": "Try asking about titles, recommendations, watchlist, plans, profiles, or downloads.",
    }
