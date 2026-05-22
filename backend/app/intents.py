"""Intent classifier for the Media chatbot."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class IntentSpec:
    name: str
    patterns: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)


INTENTS: list[IntentSpec] = [
    IntentSpec("greeting",
        patterns=[r"^\s*(hi|hello|hey|hola|namaste|good (morning|afternoon|evening))\b"],
        keywords=["hi", "hello", "hey", "hola", "namaste"]),
    IntentSpec("goodbye",
        patterns=[r"\b(bye|goodbye|see ya|see you|cya|take care)\b"],
        keywords=["bye", "goodbye"]),
    IntentSpec("thanks",
        patterns=[r"^\s*(thanks|thank you|thx|ty|appreciate it)\b"],
        keywords=["thanks", "thank"]),
    IntentSpec("search_titles",
        patterns=[
            r"\b(find|search|show|look\s+for)\b.{0,30}\b(titles?|movies?|series|shows?|films?|content|documentaries|documentary)\b",
            r"\b(any|got|do you have)\s+\w+\s+(movies?|series|shows?|films?)\b",
            r"\b(movies?|series|shows?|films?)\s+(in|about|on|with)\s+\w+",
            r"\b(crime|thriller|comedy|romance|sci[\s-]?fi|fantasy|drama|documentary|animation|action|horror|mystery)\s+(titles?|movies?|series|shows?|films?)\b",
        ],
        keywords=["find titles", "search movies", "movies", "series", "shows", "films"]),
    IntentSpec("title_detail",
        patterns=[
            r"\b(show|view|details? (of|on|for|about)|tell me about)\s+(this\s+)?(title|movie|series|show|film)",
            r"\bti-?\d{3,5}\b",
            r"\bmore (info|details|about)\s+(this|that)\s+(title|movie|series|show|film)",
        ],
        keywords=["title details", "movie details"]),
    IntentSpec("trailer",
        patterns=[
            r"\b(play|show|watch|see)\s+(the\s+)?(trailer|preview|teaser)\b",
            r"\btrailer\s+(of|for|to)\s+\w+",
            r"\b(can\s+i\s+see|got\s+a)\s+trailer\b",
        ],
        keywords=["trailer", "preview", "teaser"]),
    IntentSpec("continue_watching",
        patterns=[
            r"\b(continue|resume|pick\s+up|keep)\s+(watching|where\s+i\s+(left|stopped))\b",
            r"\bcontinue\s+watching\b",
            r"\b(my\s+)?(currently\s+watching|in\s+progress)\b",
        ],
        keywords=["continue watching", "resume", "where I left off"]),
    IntentSpec("watchlist",
        patterns=[
            r"\b(my\s+)?(watch[\s-]?list|saved|bookmarked|to[\s-]?watch)\b",
            r"\b(add|save)\s+(to\s+)?(my\s+)?watch[\s-]?list\b",
            r"\b(show|view|see)\s+(my\s+)?watch[\s-]?list\b",
        ],
        keywords=["watchlist", "my list", "saved titles"]),
    IntentSpec("downloads",
        patterns=[
            r"\b(my\s+)?downloads?\b",
            r"\b(download|get|save)\s+(this|that)\s+(for\s+)?(offline|later)\b",
            r"\b(show|view|see)\s+(my\s+)?downloads?\b",
            r"\boffline\s+(viewing|titles?|library)\b",
        ],
        keywords=["downloads", "download for offline", "my downloads"]),
    IntentSpec("recommend",
        patterns=[
            r"\b(recommend|suggest|what should i|what would you|surprise me|pick (for|something))\b",
            r"\b(don'?t know what to watch|can'?t decide)\b",
            r"\bwhat'?s good (here|tonight|today)\b",
            r"\b(top\s+picks?|trending|popular)\s+(titles?|content|movies?|series|shows?)?\b",
            r"\b(something\s+like|similar\s+to)\s+\w+",
        ],
        keywords=["recommend", "suggest", "what should I watch", "surprise me", "trending"]),
    IntentSpec("profiles",
        patterns=[
            r"\b(my\s+)?profiles?\b",
            r"\b(switch|change)\s+(to\s+)?(profile|account)\b",
            r"\b(kids|family|main)\s+profile\b",
        ],
        keywords=["profiles", "switch profile", "kids profile"]),
    IntentSpec("parental_controls",
        patterns=[
            r"\b(parental|child(ren)?)\s+(controls?|filter|protection|safety|settings?)\b",
            r"\bkids?\s+(controls?|filter|protection|safety|settings?)\b",
            r"\b(set|setup|enable|turn\s+on)\s+(parental|kids)\s+(controls?|filter|pin)\b",
            r"\bblock\s+(adult|mature|inappropriate)\s+(content|titles?)\b",
        ],
        keywords=["parental controls", "kids filter", "child protection"]),
    IntentSpec("view_plans",
        patterns=[
            r"\b(subscription|plan|pricing|tier)s?\b(?!\s+(id|am|details))",
            r"\b(upgrade|downgrade|change)\s+(my\s+)?(plan|subscription|tier)\b",
            r"\b(view|show|see)\s+(plans?|pricing|tiers?)\b",
            r"\bhow\s+much\s+(does|is)\s+(it|the\s+subscription)\b",
        ],
        keywords=["plans", "pricing", "upgrade plan"]),
    IntentSpec("current_subscription",
        patterns=[
            r"\b(my\s+)?(current\s+)?(subscription|plan)\s+(details?|info|status)\b",
            r"\bwhich\s+plan\s+am\s+i\s+on\b",
            r"\bwhat\s+plan\s+am\s+i\s+on\b",
            r"\bwhen\s+(does|will)\s+(my\s+)?subscription\s+renew\b",
            r"\bcancel\s+(my\s+)?subscription\b",
        ],
        keywords=["my subscription", "current plan", "renew", "cancel subscription"]),
    IntentSpec("devices",
        patterns=[
            r"\b(my\s+)?(devices?|logged[\s-]?in\s+devices?|connected\s+devices?)\b",
            r"\b(sign\s+out|logout|log\s+out)\s+(from|of)\s+(all|other)\s+devices?\b",
            r"\b(manage|view|show)\s+devices?\b",
        ],
        keywords=["devices", "logged in devices", "sign out devices"]),
    IntentSpec("audio_subtitles",
        patterns=[
            r"\b(audio|sound|language)\s+(track|option|settings?)\b",
            r"\b(subtitles?|cc|captions?)\s+(in|for|options?|settings?)\b",
            r"\b(change|switch)\s+(audio|language|subtitles?)\b",
            r"\bdolby\s+atmos\b",
            r"\b(hindi|tamil|telugu|bengali|english)\s+(audio|dub|dubbing|subtitles?)\b",
        ],
        keywords=["audio settings", "subtitles", "language", "captions"]),
    IntentSpec("contact_support",
        patterns=[
            r"\b(contact|talk to|speak to|reach)\s+(support|customer\s+(service|care)|help)",
            r"\b(human|real person|agent|representative)\b",
            r"\b(complaint|issue|problem|bug)\s+(with|about|on)\s+(my\s+)?(account|subscription|stream|playback)",
            r"\b(can'?t|cannot|unable to)\s+(play|stream|watch|login|log\s+in)\b",
        ],
        keywords=["support", "customer service", "complaint", "playback issue"]),
]


GENRE_KEYWORDS = {
    "Crime":       ["crime", "criminal", "noir"],
    "Thriller":    ["thriller", "thrillers", "suspense"],
    "Drama":       ["drama", "dramatic"],
    "Comedy":      ["comedy", "comedies", "funny", "humor", "humour"],
    "Romance":     ["romance", "romantic", "rom-com", "romcom"],
    "Sci-Fi":      ["sci-fi", "scifi", "sci fi", "science fiction"],
    "Fantasy":     ["fantasy", "magical"],
    "Adventure":   ["adventure"],
    "Mystery":     ["mystery", "whodunit"],
    "Animation":   ["animation", "animated", "cartoon", "anime"],
    "Family":      ["family"],
    "Documentary": ["documentary", "documentaries", "docu"],
    "Action":      ["action", "fight scene"],
    "Horror":      ["horror", "scary", "spooky"],
}


def extract_genres(text: str) -> list[str]:
    t = text.lower()
    found = []
    for genre, kws in GENRE_KEYWORDS.items():
        for kw in kws:
            if re.search(rf"\b{re.escape(kw)}\b", t):
                if genre not in found:
                    found.append(genre)
                break
    return found


def extract_title_id(text: str) -> Optional[str]:
    m = re.search(r"\bti-?(\d{3,5})\b", text.lower())
    if m:
        return f"TI-{m.group(1)}"
    return None


def extract_plan_name(text: str) -> Optional[str]:
    t = text.lower()
    for name in ["premium", "basic", "mobile"]:
        if re.search(rf"\b{name}\b", t):
            return name.capitalize()
    return None


def extract_profile_name(text: str) -> Optional[str]:
    t = text.lower()
    for name in ["main", "family", "kids", "kid"]:
        if re.search(rf"\b{name}\b", t):
            return "Kids" if name == "kid" else name.capitalize()
    return None


def extract_language(text: str) -> Optional[str]:
    t = text.lower()
    for lang in ["hindi", "english", "tamil", "telugu", "bengali", "korean", "malayalam", "marathi"]:
        if re.search(rf"\b{lang}\b", t):
            return lang.capitalize()
    return None


@dataclass
class Classification:
    intent: str
    confidence: float
    entities: dict


def classify(text: str) -> Classification:
    text_lc = text.lower().strip()
    scores: dict[str, float] = {}
    for spec in INTENTS:
        score = 0.0
        for p in spec.patterns:
            if re.search(p, text_lc, re.IGNORECASE):
                score += 2.0
        for kw in spec.keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text_lc):
                score += 0.6
        if score > 0:
            scores[spec.name] = score

    if extract_title_id(text):
        scores["title_detail"] = scores.get("title_detail", 0) + 1.5

    genres = extract_genres(text)
    if genres and not any(i in scores for i in ["title_detail", "trailer", "watchlist", "downloads", "continue_watching"]):
        scores["search_titles"] = scores.get("search_titles", 0) + 1.5

    if not scores:
        intent, conf = "unknown", 0.0
    else:
        intent = max(scores, key=scores.get)
        top = scores[intent]
        rest = sorted(scores.values(), reverse=True)[1] if len(scores) > 1 else 0.1
        conf = min(1.0, top / (top + rest))

    return Classification(
        intent=intent,
        confidence=round(conf, 2),
        entities={
            "genres":       genres,
            "title_id":     extract_title_id(text),
            "plan_name":    extract_plan_name(text),
            "profile_name": extract_profile_name(text),
            "language":     extract_language(text),
        },
    )
