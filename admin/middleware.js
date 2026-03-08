/**
 * admin/middleware.js
 * API-side middleware: key validation, rate limiting, IP blocking, logging.
 */

const store   = require("../data/store");
const keysMod = require("./keys");

// Per-key rate limit tracker (in-memory, resets each minute)
const keyRateLimits = {};
// Per-IP rate limit tracker
const ipRateLimits  = {};

function getRateLimit(key, limit) {
  const now = Date.now();
  if (!keyRateLimits[key] || keyRateLimits[key].resetTime < now) {
    keyRateLimits[key] = { current: 0, resetTime: now + 60000, limit };
  }
  return keyRateLimits[key];
}

function getIPLimit(ip, limit) {
  const now = Date.now();
  if (!ipRateLimits[ip] || ipRateLimits[ip].resetTime < now) {
    ipRateLimits[ip] = { current: 0, resetTime: now + 60000, limit };
  }
  return ipRateLimits[ip];
}

// ── IP Blocking middleware ────────────────────────────────────────────────────

function ipBlockMiddleware(req, res, next) {
  const ip      = req.ip || req.connection.remoteAddress;
  const blocked = store.blocked();
  const entry   = blocked[ip];
  if (entry) {
    if (entry.expiresAt && new Date(entry.expiresAt) < new Date()) {
      // Expired block — remove it
      delete blocked[ip];
      store.saveBlocked();
    } else {
      return res.status(403).json({
        success: false,
        error: "Your IP has been blocked",
        reason: entry.reason || "Policy violation",
        created_by: "@ftgamer2",
      });
    }
  }
  next();
}

// ── Auto-block logic ──────────────────────────────────────────────────────────

function checkAutoBlock(ip) {
  const settings = loadSettings();
  const limit    = settings.autoBlockThreshold || 200;
  const tracker  = getIPLimit(ip, 99999);
  tracker.current++;

  if (tracker.current >= limit) {
    const blocked = store.blocked();
    if (!blocked[ip]) {
      blocked[ip] = {
        reason:    `Auto-blocked: ${tracker.current} requests in 1 minute (threshold: ${limit})`,
        blockedAt: new Date().toISOString(),
        blockedBy: "auto",
        expiresAt: null,
      };
      store.saveBlocked();
      console.log(`[AutoBlock] Blocked IP: ${ip}`);
    }
  }
}

// ── Key validation middleware ─────────────────────────────────────────────────

function requireKey(req, res, next) {
  const key = req.headers["x-api-key"] || req.query.key;
  if (!key) {
    return res.status(401).json({
      success: false,
      error: "API key required",
      hint: "Pass your key via X-Api-Key header or ?key= query parameter",
      created_by: "@ftgamer2",
    });
  }

  const { valid, reason, record } = keysMod.isKeyValid(key);
  if (!valid) {
    return res.status(403).json({ success: false, error: reason, created_by: "@ftgamer2" });
  }

  // Rate limit this key
  const rl = getRateLimit(key, record.rateLimit || 1000);
  rl.current++;
  const remaining = Math.max(0, rl.limit - rl.current);

  res.set({
    "X-RateLimit-Limit":     rl.limit,
    "X-RateLimit-Remaining": remaining,
    "X-RateLimit-Reset":     Math.ceil(rl.resetTime / 1000),
  });

  if (rl.current > rl.limit) {
    return res.status(429).json({
      success: false,
      error: "Rate limit exceeded",
      resetAt: new Date(rl.resetTime).toISOString(),
      created_by: "@ftgamer2",
    });
  }

  req.apiKey    = key;
  req.apiRecord = record;
  next();
}

// ── Access logger ─────────────────────────────────────────────────────────────

function logAccess(req, res, responseTime, status, extra = {}) {
  const ip   = req.ip || req.connection.remoteAddress || "unknown";
  const key  = req.apiKey || "no-key";
  const ep   = req.path;
  const date = new Date().toISOString().slice(0, 10);

  // Stats
  const st = store.stats();
  st.apiCalls.total = (st.apiCalls.total || 0) + 1;
  st.apiCalls.byKey[key]  = (st.apiCalls.byKey[key]  || 0) + 1;
  st.apiCalls.byIP[ip]    = (st.apiCalls.byIP[ip]    || 0) + 1;
  st.apiCalls.byEndpoint[ep] = (st.apiCalls.byEndpoint[ep] || 0) + 1;
  st.apiCalls.byDate[date]   = (st.apiCalls.byDate[date]   || 0) + 1;
  store.saveStats();

  // Auto-block check
  checkAutoBlock(ip);

  // Access log entry
  const logs = store.logs();
  const entry = {
    timestamp:    new Date().toISOString(),
    key,
    ip,
    endpoint:     ep,
    number:       extra.number || null,
    responseTime: Math.round(responseTime),
    status,
  };
  logs.unshift(entry);
  if (logs.length > 5000) logs.splice(5000); // cap at 5000 entries
  store.saveLogs();
}

// ── Settings helper ───────────────────────────────────────────────────────────

let _settings = null;

function loadSettings() {
  if (_settings) return _settings;
  try {
    const fs   = require("fs");
    const path = require("path");
    const f    = path.join(__dirname, "../data/settings.json");
    if (fs.existsSync(f)) {
      _settings = JSON.parse(fs.readFileSync(f, "utf8"));
    }
  } catch {}
  if (!_settings) {
    _settings = { autoBlockThreshold: 200 };
  }
  return _settings;
}

function saveSettings(obj) {
  const fs   = require("fs");
  const path = require("path");
  _settings  = obj;
  fs.writeFileSync(
    path.join(__dirname, "../data/settings.json"),
    JSON.stringify(obj, null, 2)
  );
}

module.exports = {
  ipBlockMiddleware,
  requireKey,
  logAccess,
  loadSettings,
  saveSettings,
  keyRateLimits,
  ipRateLimits,
};
    
