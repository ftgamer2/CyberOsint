/**
 * admin/keys.js — key lifecycle management
 */

const store = require("../data/store");

// IST offset
const IST_OFFSET = 5.5 * 60 * 60 * 1000;

function nowIST() {
  return new Date(Date.now() + IST_OFFSET);
}

function toIST(isoString) {
  if (!isoString) return null;
  return new Date(new Date(isoString).getTime() + IST_OFFSET);
}

function generateKey(type) {
  const prefix = type === "trial" ? "ft-key-tr" : "ft-key-lt";
  const chars  = "abcdefghijklmnopqrstuvwxyz0123456789";
  const rand   = Array.from({ length: 12 }, () => chars[Math.floor(Math.random() * chars.length)]).join("");
  return `${prefix}-${rand}`;
}

function recountKeyStats() {
  const db = store.keys();
  const st = store.stats();
  let active = 0, suspended = 0;
  for (const k of Object.values(db.lifetime)) {
    if (k.status === "active") active++; else suspended++;
  }
  for (const k of Object.values(db.trial)) {
    if (k.status === "active") active++; else suspended++;
  }
  st.activeKeys    = active;
  st.suspendedKeys = suspended;
  store.saveStats();
}

// ── CRUD ──────────────────────────────────────────────────────────────────────

function createKey(opts = {}) {
  const db      = store.keys();
  const type    = opts.type === "trial" ? "trial" : "lifetime";
  const key     = generateKey(type);
  const now     = new Date().toISOString();

  let expiresAt = null;
  if (opts.expiresAt) {
    expiresAt = new Date(opts.expiresAt).toISOString();
  } else if (type === "trial" && opts.trialMinutes) {
    expiresAt = new Date(Date.now() + opts.trialMinutes * 60 * 1000).toISOString();
  }

  const record = {
    key,
    type,
    owner:         opts.owner         || "Unknown",
    customerName:  opts.customerName  || opts.owner || "Unknown",
    customerEmail: opts.customerEmail || "",
    price:         parseFloat(opts.price) || 0,
    notes:         opts.notes         || "",
    createdAt:     now,
    expiresAt,
    status:        "active",
    rateLimit:     parseInt(opts.rateLimit) || (type === "trial" ? 10 : 1000),
  };

  db[type][key] = record;
  store.saveKeys();
  recountKeyStats();
  return record;
}

function getKey(key) {
  const db = store.keys();
  return db.lifetime[key] || db.trial[key] || null;
}

function getAllKeys() {
  const db = store.keys();
  const all = [];
  for (const k of Object.values(db.lifetime)) all.push({ ...k, type: "lifetime" });
  for (const k of Object.values(db.trial))    all.push({ ...k, type: "trial" });
  return all.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
}

function updateKey(key, changes) {
  const db   = store.keys();
  const type = db.lifetime[key] ? "lifetime" : db.trial[key] ? "trial" : null;
  if (!type) return null;
  Object.assign(db[type][key], changes);
  store.saveKeys();
  recountKeyStats();
  return db[type][key];
}

function deleteKey(key) {
  const db   = store.keys();
  const type = db.lifetime[key] ? "lifetime" : db.trial[key] ? "trial" : null;
  if (!type) return false;
  delete db[type][key];
  store.saveKeys();
  recountKeyStats();
  return true;
}

function suspendKey(key)  { return updateKey(key, { status: "suspended" }); }
function activateKey(key) { return updateKey(key, { status: "active" }); }

function extendKey(key, daysOrDate) {
  const rec = getKey(key);
  if (!rec) return null;
  let newExpiry;
  if (typeof daysOrDate === "number") {
    const base = rec.expiresAt ? new Date(rec.expiresAt) : new Date();
    newExpiry = new Date(base.getTime() + daysOrDate * 86400000).toISOString();
  } else {
    newExpiry = new Date(daysOrDate).toISOString();
  }
  return updateKey(key, { expiresAt: newExpiry });
}

function isKeyValid(key) {
  const rec = getKey(key);
  if (!rec) return { valid: false, reason: "Key not found" };
  if (rec.status === "suspended") return { valid: false, reason: "Key suspended" };
  if (rec.expiresAt && new Date(rec.expiresAt) < new Date()) return { valid: false, reason: "Key expired" };
  return { valid: true, record: rec };
}

function searchKeys(query) {
  const q = (query || "").toLowerCase();
  return getAllKeys().filter(k =>
    k.key.toLowerCase().includes(q) ||
    k.customerName.toLowerCase().includes(q) ||
    k.customerEmail.toLowerCase().includes(q) ||
    k.owner.toLowerCase().includes(q)
  );
}

function keysExpiringIn(ms) {
  const cutoff = Date.now() + ms;
  return getAllKeys().filter(k => k.expiresAt && new Date(k.expiresAt) < cutoff && k.status === "active");
}

module.exports = {
  generateKey, createKey, getKey, getAllKeys, updateKey, deleteKey,
  suspendKey, activateKey, extendKey, isKeyValid, searchKeys, keysExpiringIn,
  toIST, nowIST,
};
