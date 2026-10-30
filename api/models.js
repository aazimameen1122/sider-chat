// Vercel serverless proxy: GET /api/models -> Sider GET /v1/models
// Needed because sider.ai.id sends no CORS headers, so browsers cannot call
// it directly. The user's key arrives in the Authorization header and is
// only forwarded — never stored or logged.
export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: { message: 'Method not allowed' } });
  }
  try {
    const upstream = await fetch('https://sider.ai.id/v1/models', {
      headers: {
        Authorization: req.headers.authorization || '',
        // Cloudflare in front of Sider blocks some default client agents.
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
      },
    });
    const text = await upstream.text();
    res.status(upstream.status);
    res.setHeader('Content-Type', 'application/json');
    return res.send(text);
  } catch (e) {
    return res.status(502).json({ error: { message: 'Upstream unreachable: ' + e.message } });
  }
}
