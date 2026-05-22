"""Media chatbot engine - safety first, then intents."""
from __future__ import annotations

from .catalog import catalog
from .intents import classify
from .safety import (
    check_safety,
    build_piracy_block, build_deepfake_block, build_news_verification_block,
    build_copyrighted_full_block, build_payment_privacy_block, build_social_engineering_block,
)
from .sessions import Session


KIDS_SAFE_RATINGS = {"U"}


def _kids_filter(items):
    return [t for t in items if t.get("rating") in KIDS_SAFE_RATINGS and t.get("kids_safe")]


def _text(c): return {"type": "text", "content": c}
def _disclaimer(c): return {"type": "disclaimer", "content": c}


def _handle_greeting(s):
    note = f" You're on the **{s.active_profile}** profile." if s.active_profile != "Main" else ""
    return [_text(
        f"Hi - I'm your Stream Assistant.{note} I can help you find titles, "
        "resume what you were watching, build a watchlist, manage downloads, and tune subscription, "
        "profile, and parental-control settings. What sounds good?"
    )], ["Recommend something", "Continue watching", "My watchlist", "Browse plans"]


def _handle_goodbye(_s):
    return [_text("Happy watching. Come back when something else catches your eye.")], []


def _handle_thanks(_s):
    return [_text("Glad to help. Anything else?")], ["Recommend something", "My watchlist", "Browse plans"]


def _handle_search_titles(c, s):
    items = catalog.titles()
    if s.active_profile == "Kids":
        items = _kids_filter(items)
    if c.entities["genres"]:
        items = [t for t in items if any(g in t["genres"] for g in c.entities["genres"])]
    lang = c.entities.get("language")
    if lang:
        items = [t for t in items if lang in t.get("languages", [])]
    if not items:
        msg = "No titles match your filters in this demo's catalog."
        if s.active_profile == "Kids":
            msg += " (Kids profile - only U-rated, kid-safe titles are listed.)"
        return [_text(msg)], ["Browse all", "Recommend something"]
    items.sort(key=lambda t: -t.get("popularity", 0))
    label = "Search results"
    if c.entities["genres"]:
        label = " / ".join(c.entities["genres"]) + " titles"
    if lang:
        label += f" ({lang})"
    return [
        _text(f"I found **{len(items)} titles** matching:"),
        {"type": "title_list", "title": label, "items": items[:8], "total": len(items)},
    ], ["See title details", "Add to watchlist", "Show trailer", "Filter by language"]


def _handle_title_detail(c, s):
    tid = c.entities.get("title_id") or s.last_title_id
    if not tid:
        return [_text("Which title? You can paste a title ID (like TI-1001) or run a search first.")], \
               ["Search titles", "Recommend something"]
    t = catalog.title(tid)
    if not t:
        return [_text(f"I couldn't find title **{tid}**.")], []
    if s.active_profile == "Kids" and not t.get("kids_safe"):
        return [_text(
            f"**{t['title']}** is rated {t['rating']} and isn't available on the Kids profile. "
            "Switch to an adult profile (with PIN) to see this title."
        )], ["Switch profile", "Kids picks", "Recommend kids titles"]
    s.last_title_id = tid
    return [
        _text(f"Here are the details for **{t['title']}**:"),
        {"type": "title_detail", "title": t},
    ], ["Play trailer", "Add to watchlist", "Download for offline", "Similar titles"]


def _handle_trailer(c, s):
    tid = c.entities.get("title_id") or s.last_title_id
    if not tid:
        return [_text("Which title's trailer would you like?")], ["Search titles"]
    t = catalog.title(tid)
    if not t:
        return [_text(f"I couldn't find title **{tid}**.")], []
    if s.active_profile == "Kids" and not t.get("kids_safe"):
        return [_text(
            f"**{t['title']}** is rated {t['rating']} - trailer isn't available on the Kids profile."
        )], ["Kids picks", "Switch profile"]
    s.last_title_id = tid
    duration = 145 if t["type"] == "movie" else 115
    return [
        _text(f"Trailer for **{t['title']}**:"),
        {"type": "trailer", "title_id": tid, "title": t["title"], "duration_seconds": duration,
         "note": "In a real platform, this would launch the trailer player with auto-quality based on your network and plan."},
    ], ["Watch full title", "Add to watchlist", "More details"]


def _handle_continue_watching(_c, s):
    items = catalog.continue_watching()
    enriched = []
    for it in items:
        t = catalog.title(it["title_id"])
        if t:
            if s.active_profile == "Kids" and not t.get("kids_safe"):
                continue
            enriched.append({**it, "_title": t})
    if not enriched:
        msg = "You don't have anything in progress yet."
        if s.active_profile == "Kids":
            msg += " (Kids profile - only U-rated continues are shown.)"
        return [_text(msg)], ["Recommend something", "Browse titles"]
    return [
        _text("Here's what you've been watching:"),
        {"type": "continue_watching", "items": enriched},
    ], ["Resume top item", "Recommend something else", "My watchlist"]


def _handle_watchlist(_c, s):
    items = catalog.watchlist()
    enriched = []
    for it in items:
        t = catalog.title(it["title_id"])
        if t:
            if s.active_profile == "Kids" and not t.get("kids_safe"):
                continue
            enriched.append({**it, "_title": t})
    if not enriched:
        return [_text("Your watchlist is empty.")], ["Recommend something", "Browse titles"]
    return [
        _text(f"You have **{len(enriched)} titles** in your watchlist:"),
        {"type": "watchlist", "items": enriched},
    ], ["Open first title", "Remove a title", "Recommend more"]


def _handle_downloads(_c, s):
    items = catalog.downloads()
    enriched = []
    for it in items:
        t = catalog.title(it["title_id"])
        if t:
            if s.active_profile == "Kids" and not t.get("kids_safe"):
                continue
            enriched.append({**it, "_title": t})
    if not enriched:
        return [_text("You don't have anything downloaded right now.")], ["Download a title", "Browse titles"]
    return [
        _text(f"You have **{len(enriched)} downloads** ready for offline viewing:"),
        {"type": "downloads", "items": enriched},
        _disclaimer("Downloads expire automatically based on licensing. Renew the download to extend access; downloads count against your plan's offline limit."),
    ], ["Delete a download", "Download more", "Manage storage"]


def _handle_recommend(c, s):
    pool = catalog.titles()
    if s.active_profile == "Kids":
        pool = _kids_filter(pool)
    if c.entities["genres"]:
        pool = [t for t in pool if any(g in t["genres"] for g in c.entities["genres"])]
    pool.sort(key=lambda t: -t.get("popularity", 0))
    picks = pool[:4]
    if not picks:
        return [_text("Nothing matches in this demo's catalog.")], ["Browse all", "My watchlist"]
    rationale = "Top picks across the catalog tonight"
    if c.entities["genres"]:
        rationale = f"Top picks matching {', '.join(c.entities['genres'])}"
    if s.active_profile == "Kids":
        rationale += " (Kids profile - U-rated only)"
    return [
        _text("Here are a few hand-picked recommendations:"),
        {"type": "recommendation", "rationale": rationale, "items": picks},
    ], ["Open first pick", "Add to watchlist", "Show more"]


def _handle_profiles(c, s):
    profiles = catalog.profiles()
    requested = c.entities.get("profile_name")
    if requested:
        target = catalog.profile(requested)
        if target:
            if target["type"] == "kids" and not s.active_profile == "Kids":
                s.active_profile = target["name"]
                return [_text(
                    f"Switched to the **{target['name']}** profile. Only U-rated, kid-safe titles are now visible."
                )], ["Kids picks", "Continue watching", "My watchlist"]
            elif target.get("pin_protected") and target["type"] == "adult":
                return [_text(
                    f"The **{target['name']}** profile is PIN-protected. In a real app this would prompt for the PIN."
                )], ["Back to current profile"]
            else:
                s.active_profile = target["name"]
                return [_text(f"Switched to the **{target['name']}** profile.")], ["Continue watching", "Recommend something"]
        return [_text(f"I couldn't find a profile named '{requested}'.")], ["Show all profiles"]
    return [
        _text(f"You have **{len(profiles)} profiles** on this account:"),
        {"type": "profiles", "items": profiles, "active_profile": s.active_profile},
    ], ["Switch to Family", "Switch to Kids", "Parental controls"]


def _handle_parental_controls(_c, _s):
    kids = next((p for p in catalog.profiles() if p["type"] == "kids"), None)
    if not kids:
        return [_text("No kids profile is set up yet.")], ["Create kids profile"]
    return [
        _text("Here are your parental-control settings:"),
        {
            "type": "parental_controls",
            "kids_profile": kids,
            "age_ratings_blocked": ["U/A 13+", "U/A 16+", "A 18+"],
            "note": (
                "Kids profile is locked to U-rated, kid-safe titles only. PIN protection prevents switching "
                "away from this profile without an adult unlocking it. Children's data privacy laws "
                "(DPDP Act in India, COPPA in the US, GDPR-K in the EU) place extra restrictions on what "
                "platforms can collect or recommend for child accounts."
            ),
        },
    ], ["Reset PIN", "Allowed ratings", "View kids picks"]


def _handle_view_plans(_c, _s):
    plans = catalog.plans()
    current = catalog.current_subscription()
    return [
        _text("Here are the available plans:"),
        {"type": "plans", "items": plans, "current_plan_id": current["plan_id"]},
        _disclaimer("Prices are demo-only and exclude applicable taxes (GST). Real platforms show the final tax-inclusive amount at checkout. Plan benefits and pricing vary by region."),
    ], ["Upgrade to Premium", "Downgrade to Mobile", "Current subscription"]


def _handle_current_subscription(_c, _s):
    sub = catalog.current_subscription()
    plan = catalog.plan(sub["plan_id"])
    if not plan:
        return [_text("Couldn't load your subscription right now.")], ["View plans"]
    return [
        _text("Here's your current subscription:"),
        {"type": "subscription", "plan": plan, "subscription": sub},
    ], ["Upgrade plan", "Cancel auto-renew", "Update payment method"]


def _handle_devices(_c, _s):
    items = catalog.devices()
    return [
        _text(f"You're signed in on **{len(items)} devices**:"),
        {"type": "devices", "items": items},
        _disclaimer("If you see a device you don't recognize, sign it out and change your password. Real platforms can also limit simultaneous streams based on your plan."),
    ], ["Sign out other devices", "Manage stream limit", "Account security"]


def _handle_audio_subtitles(_c, _s):
    return [_text(
        "Audio and subtitle tracks are available per title. For most titles in this demo's catalog:\n\n"
        "- **Audio**: English, Hindi (most titles); Tamil, Telugu, Korean (selected titles)\n"
        "- **Subtitles**: English, Hindi, Tamil, Telugu, Bengali, French, Spanish, German (varies)\n"
        "- **Audio quality**: Stereo on Mobile plan, 5.1 on Basic, Dolby Atmos on Premium\n\n"
        "To change for a specific title, open the title detail and tap the audio/subtitles icon during playback."
    )], ["Show Hindi titles", "Show Premium plan", "Open a title"]


def _handle_contact_support(_c, _s):
    return [_text(
        "Sure - for issues with playback (buffering, errors, blank screen), billing, or account access, "
        "support is the right channel. In this demo, support isn't connected to a real ticket system. "
        "In a real app, this would open a chat with a human agent or create a support ticket."
    )], ["Current subscription", "My devices", "Try restart playback"]


def _handle_unknown(_c, _s):
    return [_text(
        "I'm not sure I caught that. I can search titles, give recommendations, manage watchlist and "
        "downloads, switch profiles, or handle subscription, devices, and parental controls. "
        "Try one of the buttons below."
    )], ["Recommend something", "Search titles", "My watchlist", "Browse plans"]


class ChatbotEngine:
    def respond(self, message, session):
        sf = check_safety(message)
        if sf.flag == "social_engineering":
            return self._sr(session, "social_engineering", build_social_engineering_block(),
                            ["Search titles", "My watchlist", "Recommend something"])
        if sf.flag == "payment_privacy":
            return self._sr(session, "payment_privacy", build_payment_privacy_block(),
                            ["Update payment method", "Current subscription"])
        if sf.flag == "piracy":
            return self._sr(session, "piracy", build_piracy_block(),
                            ["Find on this platform", "Free trial info", "Similar legal titles"])
        if sf.flag == "deepfake":
            return self._sr(session, "deepfake", build_deepfake_block(),
                            ["Write fictional characters", "Recommend something", "About this platform"])
        if sf.flag == "news_verification":
            return self._sr(session, "news_verification", build_news_verification_block(),
                            ["Recommend documentaries", "Find original source", "About fact-checkers"])
        if sf.flag == "copyrighted_full":
            return self._sr(session, "copyrighted_full", build_copyrighted_full_block(),
                            ["Discuss themes", "Summarize the plot", "Where to access legally"])

        c = classify(message)
        session.last_intent = c.intent
        session.history.append({"role": "user", "text": message})
        if c.entities.get("title_id"):
            session.last_title_id = c.entities["title_id"]

        hmap = {
            "greeting":             lambda: _handle_greeting(session),
            "goodbye":              lambda: _handle_goodbye(session),
            "thanks":               lambda: _handle_thanks(session),
            "search_titles":        lambda: _handle_search_titles(c, session),
            "title_detail":         lambda: _handle_title_detail(c, session),
            "trailer":              lambda: _handle_trailer(c, session),
            "continue_watching":    lambda: _handle_continue_watching(c, session),
            "watchlist":            lambda: _handle_watchlist(c, session),
            "downloads":            lambda: _handle_downloads(c, session),
            "recommend":            lambda: _handle_recommend(c, session),
            "profiles":             lambda: _handle_profiles(c, session),
            "parental_controls":    lambda: _handle_parental_controls(c, session),
            "view_plans":           lambda: _handle_view_plans(c, session),
            "current_subscription": lambda: _handle_current_subscription(c, session),
            "devices":              lambda: _handle_devices(c, session),
            "audio_subtitles":      lambda: _handle_audio_subtitles(c, session),
            "contact_support":      lambda: _handle_contact_support(c, session),
        }
        handler = hmap.get(c.intent, lambda: _handle_unknown(c, session))
        blocks, suggestions = handler()
        return {
            "session_id":  session.session_id,
            "intent":      c.intent,
            "confidence":  c.confidence,
            "blocks":      blocks,
            "suggestions": suggestions,
            "safety_flag": None,
        }

    def _sr(self, session, flag, block, suggestions):
        return {
            "session_id":  session.session_id,
            "intent":      f"{flag}_block",
            "confidence":  1.0,
            "blocks":      [block],
            "suggestions": suggestions,
            "safety_flag": flag,
        }


engine = ChatbotEngine()
