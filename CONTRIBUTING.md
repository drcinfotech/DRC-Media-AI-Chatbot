# Contributing

Thank you for your interest in contributing to the Media AI Chatbot demo. A few specifics for this project:

## Content-safety contribution checklist

Before opening a PR that touches `backend/app/safety.py`, `intents.py`, `chatbot.py`, or the catalog, please confirm:

- [ ] **No real OTT platform names** in any new content (Netflix, Prime Video, Hotstar, Disney+, Hulu, HBO Max, Paramount+, Peacock, Zee5, SonyLIV, Voot, JioCinema, MX Player, Apple TV+, etc.).
- [ ] **No real studio names with strong trademark claims** (Marvel Studios, Lucasfilm, Pixar, DreamWorks, Warner Bros, Universal Studios, Paramount Pictures, Yash Raj Films, Dharma Productions, Red Chillies, etc.).
- [ ] **All 6 safety patterns still fire correctly**:
  - 🎬 Piracy (pirated streams, torrents, "free" of paid content, named pirate sites, DRM cracking)
  - 👤 Deepfake / impersonation (real-person scripts, voice clones, fake quotes)
  - 📰 News verification (no confident true/fake verdicts)
  - 📝 Copyrighted reproduction (no full lyrics / screenplays / chapters)
  - 💳 Payment privacy (card numbers, CVV, OTP, PIN in chat)
  - 🛡️ Social engineering (jailbreak, free-premium, parental bypass)
- [ ] **Kids-profile rating cap is preserved**: when `active_profile == "Kids"`, only titles where `rating == "U"` AND `kids_safe == true` are returned. Adult titles get a text refusal, NOT a `title_detail` block.
- [ ] **Tests pass**: `cd backend && pytest -q` shows 72 (or more) passed.

## Local development

```bash
# Backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Adding a new intent

1. Define an `IntentSpec` in `intents.py` with patterns and keywords.
2. Add a handler `_handle_<name>(c, s)` in `chatbot.py` returning `(blocks, suggestions)`.
3. Wire it into `handler_map` in `ChatbotEngine.respond`.
4. Add a test in `test_chatbot.py`.

## Adding a new block type

1. Define a Pydantic model in `models.py` and add to `MessageBlock` union.
2. Build a renderer in `frontend/src/components/Blocks.jsx` and wire into the `Block` dispatcher.

## Adding a new safety pattern

1. Add the regex to the appropriate `_PATTERNS` list in `safety.py`.
2. Add a test that asserts `check_safety("trigger phrase").flag == "category"`.
3. Add a test in `test_safety_no_false_positives` style so legitimate queries don't trip it.

## Code style

- Python: 4-space indent, type hints encouraged but not required for tests.
- JS/JSX: 2-space indent, no trailing semicolons (matches the existing style).

## Pull requests

Open against `main`. CI runs Python 3.10 / 3.11 / 3.12 × Node 18 / 20 matrix.
