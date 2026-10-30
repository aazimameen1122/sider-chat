# Sider Chat

A simple website to chat with the [Sider AI API](https://sider.ai.id/v1) — an
OpenAI-compatible API. Paste your own Sider API key in the page, pick a model,
and chat.

**Live:**
- Vercel: https://sider-chat.vercel.app
- GitHub Pages: https://aazimameen1122.github.io/sider-chat/

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

## GitHub Pages

This repo is also served by GitHub Pages at
https://aazimameen1122.github.io/sider-chat/ — and chat works there too.
Pages itself has no server side, so when the page is opened from the
`github.io` domain it automatically sends its API calls to the Vercel
deployment of this same repo (`https://sider-chat.vercel.app`), whose
`api/` functions allow cross-origin calls. Everywhere else (Vercel, local
server) the page uses its own same-origin proxy.

## Files

| File | What it is |
|---|---|
| `index.html` | The chat page (UI, model picker, system prompt, history) |
| `server.py` | Local server + Sider proxy (no dependencies) |
| `api/chat.js` | Vercel proxy for chat completions |
| `api/models.js` | Vercel proxy for the model list |
