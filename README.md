# Sider Chat

A simple website to chat with the [Sider AI API](https://sider.ai.id/v1) — an
OpenAI-compatible API. Paste your own Sider API key in the page, pick a model,
and chat.

**Models available on this API:** `deepseek-4.1-unrestricted` (default),
`gemini-3.1-pro`, `gemini-3.8-flash`, `glm-5.3-unrestricted`.

## Why is there a proxy?

`sider.ai.id` sends **no CORS headers**, so a web page in a browser cannot
call it directly — every request would be blocked. This repo includes a tiny
proxy that forwards requests from the page to Sider:

- `server.py` — for running locally (Python standard library only, nothing to install)
- `api/chat.js` + `api/models.js` — serverless functions for deploying on Vercel

Your API key is **never** embedded in the code and never stored on any
server. You paste it into the page; it stays in your own browser
(localStorage) and is only sent, per request, to Sider through the proxy.

## Run it locally

```bash
python3 server.py
```

Then open http://localhost:8000, paste your key, and hit **Test connection**.

## Deploy it (free, from this GitHub repo)

1. Go to [vercel.com](https://vercel.com) → sign in with GitHub → **Add New → Project**
2. Import this repository — no settings needed, Vercel picks up `index.html`
   and the `api/` functions automatically
3. Open your deployed URL, paste your key, chat

## Note on GitHub Pages

GitHub Pages can host the page itself, but chat will **not** work there —
Pages has no server side, and Sider's missing CORS headers block direct
browser calls. Use the local server or Vercel deploy above for a working chat.

## Files

| File | What it is |
|---|---|
| `index.html` | The chat page (UI, model picker, system prompt, history) |
| `server.py` | Local server + Sider proxy (no dependencies) |
| `api/chat.js` | Vercel proxy for chat completions |
| `api/models.js` | Vercel proxy for the model list |
