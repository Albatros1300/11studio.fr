// /api/reviews — commentaires de la page de validation, stockés dans Vercel Blob.
// GET  → { items: { <item>: [ {item, author, text, status, ts, key}, … ] } }  (tri par ts croissant)
// POST { item, author, status, text } → { entry }
// Réécrit le 28/09/2026 à partir du contrat observé en production (même format, même préfixe « reviews/ »).
const { put, list } = require("@vercel/blob");

const s = (v, max) => (v === undefined || v === null ? "" : String(v).trim().slice(0, max));

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  try {
    if (req.method === "GET") {
      const items = {};
      let cursor;
      do {
        const page = await list({ prefix: "cercle-energie/reviews/", limit: 1000, cursor });
        const entries = await Promise.all(page.blobs.map(async (b) => {
          try { const r = await fetch(b.url, { cache: "no-store" }); const j = await r.json(); return { ...j, key: j.key || b.pathname }; }
          catch (e) { return null; }
        }));
        entries.filter(Boolean).forEach((e) => { (items[e.item] = items[e.item] || []).push(e); });
        cursor = page.hasMore ? page.cursor : undefined;
      } while (cursor);
      Object.keys(items).forEach((k) => items[k].sort((a, b) => (a.ts || 0) - (b.ts || 0)));
      return res.end(JSON.stringify({ items }));
    }
    if (req.method === "POST") {
      let b = req.body; if (typeof b === "string") { try { b = JSON.parse(b); } catch (e) { b = {}; } } b = b || {};
      const item = s(b.item, 80).replace(/[^A-Za-z0-9_.-]/g, "");
      const author = s(b.author, 80), text = s(b.text, 2000), status = s(b.status, 20);
      if (!item) { res.statusCode = 400; return res.end(JSON.stringify({ error: "item manquant" })); }
      if (!author) { res.statusCode = 400; return res.end(JSON.stringify({ error: "Indiquez votre nom" })); }
      if (!status && !text) { res.statusCode = 400; return res.end(JSON.stringify({ error: "Choisissez une décision ou écrivez un commentaire" })); }
      const ts = Date.now();
      const key = `cercle-energie/reviews/${item}/${ts}-${Math.random().toString(36).slice(2, 8)}.json`;
      const entry = { item, author, text, status, ts, key };
      await put(key, JSON.stringify(entry), { access: "public", addRandomSuffix: false, contentType: "application/json" });
      res.statusCode = 201;
      return res.end(JSON.stringify({ entry }));
    }
    res.statusCode = 405; return res.end(JSON.stringify({ error: "méthode non autorisée" }));
  } catch (e) {
    console.error("reviews", e && e.message);
    res.statusCode = 500; return res.end(JSON.stringify({ error: "stockage indisponible" }));
  }
};
