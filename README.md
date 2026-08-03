# ai-assistant-bot

A Streamlit chat client for Gemini with three things layered on top of a plain chat loop:
persistent multi-session history in SQLite, PDF and image input, and a model resolver that
finds a working Gemini model at startup instead of hardcoding one.

Python · Streamlit · google-generativeai · SQLite · PyPDF2 · Pillow

---

## The part worth reading: model resolution

Gemini model IDs churn. A build pinned to `gemini-pro` stops working when that alias is
retired, and the failure is a runtime exception on the first message, not something you catch
at install time. This app resolves a model at startup instead:

```python
candidate_models = [
    'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro',
    'gemini-1.5-flash-latest', 'gemini-1.5-pro-latest',
    'models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro'
]
```

Then it asks the API what else exists and appends anything advertising `generateContent`, so
models released after this code was written are still reachable. Finally it walks the list and
**sends a one-token test generation** to each candidate, returning the first that actually
answers.

Listing a model is not the same as being able to call it — quota, region and account tier all
produce models that appear in `list_models()` and then fail on use. The test call is what makes
the fallback real rather than theoretical. Every failed attempt is collected into `debug_logs`
and surfaced in the UI, so when nothing works you can see exactly which model returned which
error instead of a blank screen.

If no candidate answers, the app stops with a clear error rather than starting into a broken
state.

## Documents: context injection, not retrieval

Worth being precise, because the two get conflated. Uploading a PDF runs
`PyPDF2.extract_text()` over every page and prepends the result to the prompt:

```python
context = f"DOCUMENT CONTEXT:\n{st.session_state.pdf_text[:10000]}\n\nQUESTION: {prompt}"
```

There is no chunking, no embedding model, no vector store and no retrieval step — the whole
document goes into the context window, truncated at 10,000 characters. For single reports and
papers that is the simpler and more accurate approach, since nothing can be missed by a bad
similarity match. It does not scale past what fits in the window, and a real retrieval layer
is the obvious next step if it needs to.

## Conversation storage

`database.py`, two tables:

| | |
|---|---|
| `sessions` | `id` (UUID), `title`, `created_at` |
| `messages` | autoincrement id, `session_id` FK, `role`, `content`, `timestamp` |

Session titles name themselves. On the first user message in a session the row count is
checked and the title is replaced with the first 30 characters of what was asked — so the
sidebar reads like a list of questions rather than "New Chat" eight times.

Deleting a session removes its messages first, then the session row.

## Other input

- **Images** — opened with Pillow and passed alongside the text prompt for visual questions.
- **Voice** — `streamlit-mic-recorder` captures audio in the browser and hands the bytes to
  the model.

---

## Running it

```bash
git clone https://github.com/Tunaycel/ai-assistant-bot
cd ai-assistant-bot
pip install -r requirements.txt
```

Create a `.env`:

```ini
GEMINI_API_KEY=your_key_here
```

A key comes from [Google AI Studio](https://aistudio.google.com/).

```bash
streamlit run app.py
```

Opens on `http://localhost:8501`. The SQLite file `chat_history_v2.db` is created on first run
in the working directory.

---

## Limitations

- Single user. There is no auth, and the database is a local file — every session in it belongs
  to whoever is running the app.
- PDF context is truncated at 10,000 characters, silently.
- `PyPDF2.extract_text()` returns nothing useful for scanned PDFs; there is no OCR fallback.
- The startup probe costs one generation call per candidate model until one succeeds.
