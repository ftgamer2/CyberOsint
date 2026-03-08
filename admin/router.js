/**
 * admin/router.js — all /ftadmin routes
 */

const express   = require("express");
const path      = require("path");
const fs        = require("fs");
const archiver  = require("archiver");
const router    = express.Router();

const store   = require("../data/store");
const keysMod = require("./keys");
const mw      = require("./middleware");

const ADMIN_PASS = process.env.ADMIN_PASSWORD || "Dilshan418@";

// ── Session check ─────────────────────────────────────────────────────────────

function requireAuth(req, res, next) {
  if (req.session && req.session.adminAuth) return next();
  return res.redirect("/ftadmin/login");
}

// ── Login rate limiter (5 attempts per 15 min) ────────────────────────────────

const loginAttempts = {};
function loginRateLimit(req, res, next) {
  const ip  = req.ip;
  const now = Date.now();
  if (!loginAttempts[ip] || loginAttempts[ip].resetTime < now) {
    loginAttempts[ip] = { count: 0, resetTime: now + 15 * 60 * 1000 };
  }
  if (loginAttempts[ip].count >= 5) {
    return res.status(429).send(loginPage("Too many attempts. Try again later.", true));
  }
  next();
}

// ── IST formatter ─────────────────────────────────────────────────────────────

function ist(iso) {
  if (!iso) return "Never";
  const d = new Date(new Date(iso).getTime() + 5.5 * 3600000);
  return d.toISOString().replace("T", " ").slice(0, 19) + " IST";
}

function istShort(iso) {
  if (!iso) return "—";
  const d = new Date(new Date(iso).getTime() + 5.5 * 3600000);
  return d.toISOString().slice(0, 10);
}

// ── HTML helpers ──────────────────────────────────────────────────────────────

function layout(title, body, activePage = "") {
  const nav = [
    { href: "/ftadmin/dashboard", icon: "⬡", label: "Dashboard", id: "dashboard" },
    { href: "/ftadmin/keys",      icon: "◈", label: "Keys",      id: "keys" },
    { href: "/ftadmin/ips",       icon: "⊗", label: "Blocked IPs", id: "ips" },
    { href: "/ftadmin/logs",      icon: "≡", label: "Logs",      id: "logs" },
    { href: "/ftadmin/settings",  icon: "⚙", label: "Settings",  id: "settings" },
  ].map(n => `
    <a href="${n.href}" class="nav-item ${activePage === n.id ? "active" : ""}">
      <span class="nav-icon">${n.icon}</span>
      <span class="nav-label">${n.label}</span>
    </a>`).join("");

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title} — ftgamer2 Admin</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<style>
  :root {
    --bg:      #0a0a0f;
    --bg2:     #0f0f1a;
    --bg3:     #141424;
    --border:  #1e1e35;
    --accent:  #7c3aed;
    --accent2: #a855f7;
    --green:   #10b981;
    --red:     #ef4444;
    --yellow:  #f59e0b;
    --text:    #e2e8f0;
    --muted:   #64748b;
    --card:    #0d0d1f;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; font-family: 'Space Grotesk', sans-serif; background: var(--bg); color: var(--text); }
  a { color: var(--accent2); text-decoration: none; }

  /* Layout */
  .shell { display: flex; height: 100vh; overflow: hidden; }
  .sidebar {
    width: 200px; min-width: 200px; background: var(--bg2);
    border-right: 1px solid var(--border); display: flex; flex-direction: column;
    padding: 20px 0;
  }
  .sidebar-brand {
    padding: 0 20px 24px; border-bottom: 1px solid var(--border);
    font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--muted);
    letter-spacing: 2px; text-transform: uppercase;
  }
  .sidebar-brand span { display: block; font-size: 16px; font-weight: 700; color: var(--accent2); letter-spacing: 0; }
  .nav-item {
    display: flex; align-items: center; gap: 10px; padding: 10px 20px;
    color: var(--muted); font-size: 13px; font-weight: 500; transition: all .15s;
    border-left: 2px solid transparent;
  }
  .nav-item:hover { color: var(--text); background: var(--bg3); }
  .nav-item.active { color: var(--accent2); border-left-color: var(--accent2); background: rgba(124,58,237,.08); }
  .nav-icon { font-size: 16px; width: 20px; text-align: center; }
  .sidebar-bottom { margin-top: auto; padding: 20px; border-top: 1px solid var(--border); }
  .logout-btn {
    display: block; text-align: center; padding: 8px; border-radius: 6px;
    background: rgba(239,68,68,.1); color: var(--red); font-size: 12px;
    border: 1px solid rgba(239,68,68,.2); transition: all .15s;
  }
  .logout-btn:hover { background: rgba(239,68,68,.2); }

  /* Main content */
  .main { flex: 1; overflow-y: auto; display: flex; flex-direction: column; }
  .topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 28px; border-bottom: 1px solid var(--border);
    background: var(--bg2); position: sticky; top: 0; z-index: 100;
  }
  .topbar-title { font-size: 16px; font-weight: 600; }
  .topbar-meta { font-size: 12px; color: var(--muted); font-family: 'JetBrains Mono', monospace; }
  .page { padding: 24px 28px; flex: 1; }

  /* Cards */
  .card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 10px; padding: 20px; margin-bottom: 20px;
  }
  .card-title { font-size: 12px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 1px; color: var(--muted); margin-bottom: 16px; }

  /* Stat grid */
  .stat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 14px; margin-bottom: 24px; }
  .stat-card {
    background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    padding: 18px; position: relative; overflow: hidden;
  }
  .stat-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: var(--accent);
  }
  .stat-card.green::before { background: var(--green); }
  .stat-card.red::before   { background: var(--red); }
  .stat-card.yellow::before { background: var(--yellow); }
  .stat-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
  .stat-value { font-size: 28px; font-weight: 700; font-family: 'JetBrains Mono', monospace;
    margin: 6px 0 2px; color: var(--text); }
  .stat-sub { font-size: 11px; color: var(--muted); }

  /* Table */
  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { text-align: left; padding: 10px 12px; font-size: 11px; text-transform: uppercase;
    letter-spacing: 1px; color: var(--muted); border-bottom: 1px solid var(--border); font-weight: 600; }
  td { padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,.04);
    vertical-align: middle; font-family: 'JetBrains Mono', monospace; font-size: 12px; }
  tr:hover td { background: rgba(255,255,255,.02); }
  .td-name { font-family: 'Space Grotesk', sans-serif; font-size: 13px; }

  /* Badges */
  .badge {
    display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px;
    font-weight: 600; letter-spacing: .5px; text-transform: uppercase;
  }
  .badge-active   { background: rgba(16,185,129,.15); color: var(--green); border: 1px solid rgba(16,185,129,.2); }
  .badge-suspended { background: rgba(239,68,68,.15); color: var(--red); border: 1px solid rgba(239,68,68,.2); }
  .badge-trial    { background: rgba(245,158,11,.15); color: var(--yellow); border: 1px solid rgba(245,158,11,.2); }
  .badge-lifetime { background: rgba(168,85,247,.15); color: var(--accent2); border: 1px solid rgba(168,85,247,.2); }
  .badge-expired  { background: rgba(100,116,139,.15); color: var(--muted); border: 1px solid rgba(100,116,139,.2); }

  /* Forms */
  .form-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px; }
  .form-group { display: flex; flex-direction: column; gap: 6px; }
  label { font-size: 12px; color: var(--muted); font-weight: 500; }
  input, select, textarea {
    background: var(--bg3); border: 1px solid var(--border); border-radius: 6px;
    padding: 9px 12px; color: var(--text); font-size: 13px; font-family: 'JetBrains Mono', monospace;
    transition: border-color .15s; outline: none;
  }
  input:focus, select:focus, textarea:focus { border-color: var(--accent2); }
  select option { background: var(--bg3); }
  textarea { resize: vertical; min-height: 80px; font-family: 'Space Grotesk', sans-serif; }

  /* Buttons */
  .btn {
    display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px;
    border-radius: 6px; font-size: 13px; font-weight: 500; cursor: pointer;
    border: none; transition: all .15s; font-family: 'Space Grotesk', sans-serif;
  }
  .btn-primary { background: var(--accent); color: #fff; }
  .btn-primary:hover { background: var(--accent2); }
  .btn-danger  { background: rgba(239,68,68,.15); color: var(--red); border: 1px solid rgba(239,68,68,.25); }
  .btn-danger:hover { background: rgba(239,68,68,.25); }
  .btn-success { background: rgba(16,185,129,.15); color: var(--green); border: 1px solid rgba(16,185,129,.25); }
  .btn-success:hover { background: rgba(16,185,129,.25); }
  .btn-ghost { background: transparent; color: var(--muted); border: 1px solid var(--border); }
  .btn-ghost:hover { color: var(--text); border-color: var(--muted); }
  .btn-sm { padding: 5px 10px; font-size: 11px; }

  /* Search */
  .search-row { display: flex; gap: 10px; margin-bottom: 16px; align-items: center; flex-wrap: wrap; }
  .search-row input { flex: 1; min-width: 200px; }

  /* Alert */
  .alert { padding: 12px 16px; border-radius: 8px; font-size: 13px; margin-bottom: 16px; }
  .alert-success { background: rgba(16,185,129,.1); border: 1px solid rgba(16,185,129,.2); color: var(--green); }
  .alert-error   { background: rgba(239,68,68,.1);  border: 1px solid rgba(239,68,68,.2);  color: var(--red); }

  /* Toast */
  #toast-container { position: fixed; bottom: 24px; right: 24px; z-index: 9999; display: flex; flex-direction: column; gap: 8px; }
  .toast {
    padding: 12px 18px; border-radius: 8px; font-size: 13px; font-weight: 500;
    animation: slide-in .2s ease; box-shadow: 0 8px 24px rgba(0,0,0,.4);
    min-width: 220px;
  }
  .toast-success { background: rgba(16,185,129,.9); color: #fff; }
  .toast-error   { background: rgba(239,68,68,.9);  color: #fff; }
  @keyframes slide-in { from { transform: translateX(120%); opacity: 0; } to { transform: none; opacity: 1; } }

  /* Chart */
  .chart-wrap { height: 200px; position: relative; }

  /* Two col layout */
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  @media (max-width: 900px) { .two-col { grid-template-columns: 1fr; } .sidebar { width: 60px; } .nav-label { display: none; } .sidebar-brand span { display: none; } }

  /* Expiry warning */
  .expiry-warn { color: var(--yellow); }
  .expiry-expired { color: var(--red); }

  /* Code */
  code { font-family: 'JetBrains Mono', monospace; background: var(--bg3); padding: 2px 6px; border-radius: 4px; font-size: 11px; }
</style>
</head>
<body>
<div class="shell">
  <aside class="sidebar">
    <div class="sidebar-brand">
      <span>@ftgamer2</span>
      API Admin
    </div>
    <nav style="flex:1;padding-top:12px">
      ${nav}
    </nav>
    <div class="sidebar-bottom">
      <a href="/ftadmin/logout" class="logout-btn">Sign Out</a>
    </div>
  </aside>
  <div class="main">
    <div class="topbar">
      <div class="topbar-title">${title}</div>
      <div class="topbar-meta" id="live-time"></div>
    </div>
    <div class="page">
      ${body}
    </div>
  </div>
</div>
<div id="toast-container"></div>
<script>
  // Live clock
  function tick() {
    const el = document.getElementById('live-time');
    if (el) {
      const now = new Date(Date.now() + 5.5*3600000);
      el.textContent = now.toISOString().replace('T',' ').slice(0,19) + ' IST';
    }
  }
  tick(); setInterval(tick, 1000);

  // Toast
  function toast(msg, type='success') {
    const c = document.getElementById('toast-container');
    const t = document.createElement('div');
    t.className = 'toast toast-' + type;
    t.textContent = msg;
    c.appendChild(t);
    setTimeout(() => t.remove(), 3000);
  }

  // Confirm wrapper
  function confirmAction(msg, form) {
    if (confirm(msg)) form.submit();
  }
</script>
</body>
</html>`;
}

function loginPage(error = "", locked = false) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin Login</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { min-height: 100vh; background: #0a0a0f; display: flex; align-items: center; justify-content: center; font-family: 'Space Grotesk', sans-serif; color: #e2e8f0; }
  .box { width: 380px; background: #0d0d1f; border: 1px solid #1e1e35; border-radius: 12px; padding: 40px; }
  .logo { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #64748b; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; }
  h1 { font-size: 22px; font-weight: 700; margin-bottom: 32px; }
  h1 span { color: #a855f7; }
  label { font-size: 12px; color: #64748b; display: block; margin-bottom: 6px; }
  input { width: 100%; background: #141424; border: 1px solid #1e1e35; border-radius: 6px; padding: 11px 14px; color: #e2e8f0; font-size: 14px; font-family: 'JetBrains Mono', monospace; outline: none; transition: border-color .15s; }
  input:focus { border-color: #7c3aed; }
  button { width: 100%; margin-top: 20px; padding: 12px; background: #7c3aed; color: #fff; border: none; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; font-family: 'Space Grotesk', sans-serif; transition: background .15s; }
  button:hover { background: #a855f7; }
  .err { margin-top: 14px; padding: 10px 14px; background: rgba(239,68,68,.1); border: 1px solid rgba(239,68,68,.2); border-radius: 6px; font-size: 13px; color: #ef4444; }
  .form-group { margin-bottom: 16px; }
</style>
</head>
<body>
<div class="box">
  <div class="logo">@ftgamer2</div>
  <h1>Admin <span>Panel</span></h1>
  ${error ? `<div class="err">${error}</div>` : ""}
  ${locked ? "" : `
  <form method="POST" action="/ftadmin/login">
    <div class="form-group">
      <label>Password</label>
      <input type="password" name="password" placeholder="Enter admin password" autofocus required>
    </div>
    <button type="submit">Sign In</button>
  </form>`}
</div>
</body>
</html>`;
}

// ── Helper: key expiry status ─────────────────────────────────────────────────

function expiryStatus(k) {
  if (!k.expiresAt) return `<span class="badge badge-lifetime">Never</span>`;
  const diff = new Date(k.expiresAt) - Date.now();
  const cls  = diff < 0 ? "badge-expired expiry-expired" : diff < 86400000 ? "badge-trial expiry-warn" : "";
  return `<span class="${cls ? "badge " + cls : ""}">${ist(k.expiresAt)}</span>`;
}

// ── Routes ────────────────────────────────────────────────────────────────────

// GET /ftadmin → redirect
router.get("/", requireAuth, (req, res) => res.redirect("/ftadmin/dashboard"));

// GET /ftadmin/login
router.get("/login", (req, res) => {
  if (req.session && req.session.adminAuth) return res.redirect("/ftadmin/dashboard");
  res.send(loginPage());
});

// POST /ftadmin/login
router.post("/login", loginRateLimit, (req, res) => {
  const ip = req.ip;
  if (!loginAttempts[ip]) loginAttempts[ip] = { count: 0, resetTime: Date.now() + 15*60000 };
  if (req.body.password === ADMIN_PASS) {
    req.session.adminAuth = true;
    req.session.loginTime = Date.now();
    loginAttempts[ip] = { count: 0, resetTime: Date.now() + 15*60000 };
    return res.redirect("/ftadmin/dashboard");
  }
  loginAttempts[ip].count++;
  const left = 5 - loginAttempts[ip].count;
  res.send(loginPage(`Wrong password. ${left > 0 ? left + " attempt(s) left." : "Locked out."}`));
});

// GET /ftadmin/logout
router.get("/logout", (req, res) => {
  req.session.destroy();
  res.redirect("/ftadmin/login");
});

// ── Dashboard ──────────────────────────────────────────────────────────────────

router.get("/dashboard", requireAuth, (req, res) => {
  const st    = store.stats();
  const today = new Date().toISOString().slice(0, 10);
  const todayCount = st.apiCalls.byDate[today] || 0;

  // Week count
  const weekCount = Object.entries(st.apiCalls.byDate)
    .filter(([d]) => {
      const diff = (Date.now() - new Date(d).getTime()) / 86400000;
      return diff <= 7;
    })
    .reduce((s, [, v]) => s + v, 0);

  // Top keys
  const topKeys = Object.entries(st.apiCalls.byKey)
    .sort((a, b) => b[1] - a[1]).slice(0, 10);

  // Top IPs
  const topIPs = Object.entries(st.apiCalls.byIP)
    .sort((a, b) => b[1] - a[1]).slice(0, 10);

  // Expiring soon (24h)
  const expiringSoon = keysMod.keysExpiringIn(24 * 3600000);

  // Recent keys
  const recentKeys = keysMod.getAllKeys().slice(0, 5);

  // Chart data (last 7 days)
  const chartLabels = [];
  const chartData   = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date(Date.now() - i * 86400000).toISOString().slice(0, 10);
    chartLabels.push(d.slice(5));
    chartData.push(st.apiCalls.byDate[d] || 0);
  }

  const body = `
    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-label">Total Calls</div>
        <div class="stat-value">${(st.apiCalls.total || 0).toLocaleString()}</div>
        <div class="stat-sub">All time</div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">Today</div>
        <div class="stat-value">${todayCount.toLocaleString()}</div>
        <div class="stat-sub">API calls</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">This Week</div>
        <div class="stat-value">${weekCount.toLocaleString()}</div>
        <div class="stat-sub">Last 7 days</div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">Active Keys</div>
        <div class="stat-value">${st.activeKeys || 0}</div>
        <div class="stat-sub">Live</div>
      </div>
      <div class="stat-card red">
        <div class="stat-label">Suspended</div>
        <div class="stat-value">${st.suspendedKeys || 0}</div>
        <div class="stat-sub">Keys</div>
      </div>
      <div class="stat-card yellow">
        <div class="stat-label">Revenue</div>
        <div class="stat-value">₹${(st.totalRevenue || 0).toLocaleString()}</div>
        <div class="stat-sub">Total tracked</div>
      </div>
    </div>

    ${expiringSoon.length ? `
    <div class="alert alert-error">
      ⚠ ${expiringSoon.length} key(s) expiring in the next 24 hours:
      ${expiringSoon.map(k => `<code>${k.key}</code>`).join(", ")}
    </div>` : ""}

    <div class="two-col">
      <div class="card">
        <div class="card-title">API Calls — Last 7 Days</div>
        <div class="chart-wrap">
          <canvas id="usageChart"></canvas>
        </div>
      </div>

      <div class="card">
        <div class="card-title">Revenue Tracker</div>
        <form method="POST" action="/ftadmin/dashboard/revenue">
          <div class="form-group" style="margin-bottom:12px">
            <label>Update Total Revenue (₹)</label>
            <input type="number" name="revenue" value="${st.totalRevenue || 0}" min="0" step="0.01">
          </div>
          <button type="submit" class="btn btn-primary btn-sm">Update</button>
        </form>
      </div>
    </div>

    <div class="two-col">
      <div class="card">
        <div class="card-title">Top 10 Keys by Usage</div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>#</th><th>Key</th><th>Calls</th></tr></thead>
            <tbody>
              ${topKeys.length ? topKeys.map(([k, v], i) => `
              <tr>
                <td>${i + 1}</td>
                <td><code>${k}</code></td>
                <td>${v.toLocaleString()}</td>
              </tr>`).join("") : "<tr><td colspan=3 style='color:var(--muted)'>No data yet</td></tr>"}
            </tbody>
          </table>
        </div>
      </div>

      <div class="card">
        <div class="card-title">Top 10 IPs by Usage</div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>#</th><th>IP</th><th>Calls</th></tr></thead>
            <tbody>
              ${topIPs.length ? topIPs.map(([ip, v], i) => `
              <tr>
                <td>${i + 1}</td>
                <td><code>${ip}</code></td>
                <td>${v.toLocaleString()}</td>
              </tr>`).join("") : "<tr><td colspan=3 style='color:var(--muted)'>No data yet</td></tr>"}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Recently Created Keys</div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Key</th><th>Owner</th><th>Type</th><th>Status</th><th>Created</th></tr></thead>
          <tbody>
            ${recentKeys.length ? recentKeys.map(k => `
            <tr>
              <td><code>${k.key}</code></td>
              <td class="td-name">${k.customerName}</td>
              <td><span class="badge badge-${k.type}">${k.type}</span></td>
              <td><span class="badge badge-${k.status}">${k.status}</span></td>
              <td>${ist(k.createdAt)}</td>
            </tr>`).join("") : "<tr><td colspan=5 style='color:var(--muted)'>No keys yet</td></tr>"}
          </tbody>
        </table>
      </div>
    </div>

    <script>
    new Chart(document.getElementById('usageChart'), {
      type: 'bar',
      data: {
        labels: ${JSON.stringify(chartLabels)},
        datasets: [{
          label: 'API Calls',
          data: ${JSON.stringify(chartData)},
          backgroundColor: 'rgba(124,58,237,0.5)',
          borderColor: '#7c3aed',
          borderWidth: 1,
          borderRadius: 4,
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: '#64748b' }, grid: { color: '#1e1e35' } },
          y: { ticks: { color: '#64748b' }, grid: { color: '#1e1e35' }, beginAtZero: true }
        }
      }
    });
    setTimeout(() => location.reload(), 30000);
    </script>
  `;
  res.send(layout("Dashboard", body, "dashboard"));
});

router.post("/dashboard/revenue", requireAuth, (req, res) => {
  const st = store.stats();
  st.totalRevenue = parseFloat(req.body.revenue) || 0;
  store.saveStats();
  res.redirect("/ftadmin/dashboard");
});

// ── Keys List ──────────────────────────────────────────────────────────────────

router.get("/keys", requireAuth, (req, res) => {
  const q    = req.query.q || "";
  const all  = q ? keysMod.searchKeys(q) : keysMod.getAllKeys();
  const msg  = req.query.msg || "";
  const err  = req.query.err || "";
  const st   = store.stats();

  const rows = all.map(k => {
    const calls = (st.apiCalls.byKey[k.key] || 0);
    const isExpired = k.expiresAt && new Date(k.expiresAt) < new Date();
    return `
    <tr>
      <td><code>${k.key}</code></td>
      <td class="td-name">${k.customerName}<br><small style="color:var(--muted)">${k.customerEmail}</small></td>
      <td><span class="badge badge-${k.type}">${k.type}</span></td>
      <td><span class="badge badge-${isExpired ? "expired" : k.status}">${isExpired ? "expired" : k.status}</span></td>
      <td>${expiryStatus(k)}</td>
      <td>${calls.toLocaleString()}</td>
      <td>₹${k.price || 0}</td>
      <td style="white-space:nowrap">
        <a href="/ftadmin/keys/edit/${k.key}" class="btn btn-ghost btn-sm">Edit</a>
        <form method="POST" action="/ftadmin/keys/${k.status === "active" ? "suspend" : "activate"}/${k.key}" style="display:inline">
          <button class="btn btn-sm ${k.status === "active" ? "btn-danger" : "btn-success"}">${k.status === "active" ? "Suspend" : "Activate"}</button>
        </form>
        <form method="POST" action="/ftadmin/keys/delete/${k.key}" style="display:inline" onsubmit="return confirm('Delete key ${k.key}?')">
          <button class="btn btn-danger btn-sm">Delete</button>
        </form>
      </td>
    </tr>`;
  }).join("");

  const body = `
    ${msg ? `<div class="alert alert-success">${msg}</div>` : ""}
    ${err ? `<div class="alert alert-error">${err}</div>` : ""}

    <div style="display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap;align-items:center">
      <a href="/ftadmin/keys/create" class="btn btn-primary">+ New Key</a>
      <a href="/ftadmin/keys/export" class="btn btn-ghost">↓ Export CSV</a>
    </div>

    <div class="card">
      <div class="search-row">
        <form method="GET" style="display:flex;gap:8px;flex:1;flex-wrap:wrap">
          <input name="q" value="${q}" placeholder="Search by name, email or key…">
          <button type="submit" class="btn btn-ghost">Search</button>
          ${q ? `<a href="/ftadmin/keys" class="btn btn-ghost">Clear</a>` : ""}
        </form>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Key</th><th>Customer</th><th>Type</th><th>Status</th><th>Expires (IST)</th><th>Calls</th><th>Price</th><th>Actions</th></tr></thead>
          <tbody>
            ${rows || `<tr><td colspan=8 style="color:var(--muted);text-align:center;padding:24px">No keys found</td></tr>`}
          </tbody>
        </table>
      </div>
    </div>
  `;
  res.send(layout("Keys", body, "keys"));
});

// Create key form
router.get("/keys/create", requireAuth, (req, res) => {
  const body = `
    <div class="card">
      <div class="card-title">Create New Key</div>
      <form method="POST" action="/ftadmin/keys/create">
        <div class="form-grid">
          <div class="form-group">
            <label>Key Type</label>
            <select name="type" id="type-sel" onchange="toggleExpiry()">
              <option value="lifetime">Lifetime</option>
              <option value="trial">Trial</option>
            </select>
          </div>
          <div class="form-group">
            <label>Customer Name</label>
            <input type="text" name="customerName" placeholder="e.g. John Doe" required>
          </div>
          <div class="form-group">
            <label>Customer Email</label>
            <input type="email" name="customerEmail" placeholder="john@example.com">
          </div>
          <div class="form-group">
            <label>Price Paid (₹)</label>
            <input type="number" name="price" placeholder="0" min="0" step="0.01">
          </div>
          <div class="form-group" id="expiry-group">
            <label>Expiry Date/Time (IST)</label>
            <input type="datetime-local" name="expiresAt">
          </div>
          <div class="form-group" id="trial-mins" style="display:none">
            <label>Trial Duration (minutes)</label>
            <input type="number" name="trialMinutes" placeholder="60" min="1">
          </div>
          <div class="form-group">
            <label>Rate Limit (req/min)</label>
            <input type="number" name="rateLimit" placeholder="1000" min="1" value="1000">
          </div>
          <div class="form-group" style="grid-column:1/-1">
            <label>Notes</label>
            <textarea name="notes" placeholder="Optional notes about this key / customer…"></textarea>
          </div>
        </div>
        <div style="margin-top:20px;display:flex;gap:10px">
          <button type="submit" class="btn btn-primary">Create Key</button>
          <a href="/ftadmin/keys" class="btn btn-ghost">Cancel</a>
        </div>
      </form>
    </div>
    <script>
    function toggleExpiry() {
      const t = document.getElementById('type-sel').value;
      document.getElementById('expiry-group').style.display = t==='trial' ? 'none' : 'flex';
      document.getElementById('trial-mins').style.display  = t==='trial' ? 'flex' : 'none';
    }
    </script>
  `;
  res.send(layout("Create Key", body, "keys"));
});

router.post("/keys/create", requireAuth, (req, res) => {
  try {
    const k = keysMod.createKey(req.body);
    res.redirect(`/ftadmin/keys?msg=Key ${k.key} created successfully`);
  } catch (e) {
    res.redirect(`/ftadmin/keys?err=${encodeURIComponent(e.message)}`);
  }
});

// Edit key
router.get("/keys/edit/:key", requireAuth, (req, res) => {
  const k = keysMod.getKey(req.params.key);
  if (!k) return res.redirect("/ftadmin/keys?err=Key not found");

  const expiryIST = k.expiresAt
    ? new Date(new Date(k.expiresAt).getTime() + 5.5*3600000).toISOString().slice(0,16)
    : "";

  const body = `
    <div class="card">
      <div class="card-title">Edit Key — <code>${k.key}</code></div>
      <form method="POST" action="/ftadmin/keys/edit/${k.key}">
        <div class="form-grid">
          <div class="form-group">
            <label>Customer Name</label>
            <input type="text" name="customerName" value="${k.customerName || ""}">
          </div>
          <div class="form-group">
            <label>Customer Email</label>
            <input type="email" name="customerEmail" value="${k.customerEmail || ""}">
          </div>
          <div class="form-group">
            <label>Price (₹)</label>
            <input type="number" name="price" value="${k.price || 0}" min="0" step="0.01">
          </div>
          <div class="form-group">
            <label>Rate Limit (req/min)</label>
            <input type="number" name="rateLimit" value="${k.rateLimit || 1000}" min="1">
          </div>
          <div class="form-group">
            <label>Expiry Date/Time (IST)</label>
            <input type="datetime-local" name="expiresAt" value="${expiryIST}">
          </div>
          <div class="form-group">
            <label>Status</label>
            <select name="status">
              <option value="active" ${k.status === "active" ? "selected" : ""}>Active</option>
              <option value="suspended" ${k.status === "suspended" ? "selected" : ""}>Suspended</option>
            </select>
          </div>
          <div class="form-group" style="grid-column:1/-1">
            <label>Notes</label>
            <textarea name="notes">${k.notes || ""}</textarea>
          </div>
        </div>
        <div style="margin-top:20px;display:flex;gap:10px">
          <button type="submit" class="btn btn-primary">Save Changes</button>
          <a href="/ftadmin/keys" class="btn btn-ghost">Cancel</a>
        </div>
      </form>
    </div>

    <div class="card" style="margin-top:20px">
      <div class="card-title">Extend Expiry</div>
      <form method="POST" action="/ftadmin/keys/extend/${k.key}" style="display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap">
        <div class="form-group">
          <label>Add Days</label>
          <input type="number" name="days" placeholder="30" min="1" style="width:100px">
        </div>
        <button type="submit" class="btn btn-success">Extend</button>
      </form>
    </div>
  `;
  res.send(layout(`Edit Key`, body, "keys"));
});

router.post("/keys/edit/:key", requireAuth, (req, res) => {
  const { customerName, customerEmail, price, rateLimit, expiresAt, status, notes } = req.body;
  // Convert IST input back to UTC
  const expiresUTC = expiresAt ? new Date(new Date(expiresAt).getTime() - 5.5*3600000).toISOString() : null;
  keysMod.updateKey(req.params.key, { customerName, customerEmail, price: parseFloat(price)||0, rateLimit: parseInt(rateLimit)||1000, expiresAt: expiresUTC, status, notes });
  res.redirect("/ftadmin/keys?msg=Key updated");
});

router.post("/keys/extend/:key", requireAuth, (req, res) => {
  keysMod.extendKey(req.params.key, parseInt(req.body.days) || 30);
  res.redirect(`/ftadmin/keys/edit/${req.params.key}?msg=Expiry extended`);
});

router.post("/keys/suspend/:key",  requireAuth, (req, res) => { keysMod.suspendKey(req.params.key);  res.redirect("/ftadmin/keys?msg=Key suspended"); });
router.post("/keys/activate/:key", requireAuth, (req, res) => { keysMod.activateKey(req.params.key); res.redirect("/ftadmin/keys?msg=Key activated"); });
router.post("/keys/delete/:key",   requireAuth, (req, res) => { keysMod.deleteKey(req.params.key);   res.redirect("/ftadmin/keys?msg=Key deleted"); });

// Export CSV
router.get("/keys/export", requireAuth, (req, res) => {
  const all = keysMod.getAllKeys();
  const headers = ["key","type","customerName","customerEmail","price","status","createdAt","expiresAt","rateLimit","notes"];
  const csv = [
    headers.join(","),
    ...all.map(k => headers.map(h => JSON.stringify(k[h] ?? "")).join(","))
  ].join("\n");
  res.setHeader("Content-Disposition", "attachment; filename=keys.csv");
  res.setHeader("Content-Type", "text/csv");
  res.send(csv);
});

// ── Blocked IPs ────────────────────────────────────────────────────────────────

router.get("/ips", requireAuth, (req, res) => {
  const blocked = store.blocked();
  const msg = req.query.msg || "";
  const err = req.query.err || "";

  const rows = Object.entries(blocked).map(([ip, info]) => {
    const isExpired = info.expiresAt && new Date(info.expiresAt) < new Date();
    return `
    <tr>
      <td><code>${ip}</code></td>
      <td>${info.reason || "—"}</td>
      <td><span class="badge badge-${isExpired ? "expired" : "suspended"}">${isExpired ? "Expired" : "Active"}</span></td>
      <td>${ist(info.blockedAt)}</td>
      <td>${ist(info.expiresAt)}</td>
      <td>${info.blockedBy || "admin"}</td>
      <td>
        <form method="POST" action="/ftadmin/ips/unblock" style="display:inline">
          <input type="hidden" name="ip" value="${ip}">
          <button class="btn btn-success btn-sm">Unblock</button>
        </form>
      </td>
    </tr>`;
  }).join("");

  const body = `
    ${msg ? `<div class="alert alert-success">${msg}</div>` : ""}
    ${err ? `<div class="alert alert-error">${err}</div>` : ""}

    <div class="card">
      <div class="card-title">Block an IP</div>
      <form method="POST" action="/ftadmin/ips/block">
        <div class="form-grid">
          <div class="form-group">
            <label>IP Address</label>
            <input type="text" name="ip" placeholder="1.2.3.4" required>
          </div>
          <div class="form-group">
            <label>Reason</label>
            <input type="text" name="reason" placeholder="Abuse / spam…" required>
          </div>
          <div class="form-group">
            <label>Expires (IST, leave blank = permanent)</label>
            <input type="datetime-local" name="expiresAt">
          </div>
        </div>
        <div style="margin-top:14px">
          <button type="submit" class="btn btn-danger">Block IP</button>
        </div>
      </form>
    </div>

    <div class="card">
      <div class="card-title">Blocked IPs (${Object.keys(blocked).length})</div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>IP</th><th>Reason</th><th>Status</th><th>Blocked At</th><th>Expires</th><th>By</th><th>Action</th></tr></thead>
          <tbody>
            ${rows || `<tr><td colspan=7 style="color:var(--muted);text-align:center;padding:24px">No blocked IPs</td></tr>`}
          </tbody>
        </table>
      </div>
    </div>
  `;
  res.send(layout("Blocked IPs", body, "ips"));
});

router.post("/ips/block", requireAuth, (req, res) => {
  const { ip, reason, expiresAt } = req.body;
  if (!ip) return res.redirect("/ftadmin/ips?err=IP required");
  const blocked = store.blocked();
  const expiresUTC = expiresAt ? new Date(new Date(expiresAt).getTime() - 5.5*3600000).toISOString() : null;
  blocked[ip] = { reason, blockedAt: new Date().toISOString(), blockedBy: "admin", expiresAt: expiresUTC };
  store.saveBlocked();
  res.redirect("/ftadmin/ips?msg=IP blocked successfully");
});

router.post("/ips/unblock", requireAuth, (req, res) => {
  const blocked = store.blocked();
  delete blocked[req.body.ip];
  store.saveBlocked();
  res.redirect("/ftadmin/ips?msg=IP unblocked");
});

// ── Logs ───────────────────────────────────────────────────────────────────────

router.get("/logs", requireAuth, (req, res) => {
  const { key: fKey, ip: fIP, date: fDate } = req.query;
  store.reloadLogs();
  let logs = store.logs();

  if (fKey)  logs = logs.filter(l => l.key  && l.key.includes(fKey));
  if (fIP)   logs = logs.filter(l => l.ip   && l.ip.includes(fIP));
  if (fDate) logs = logs.filter(l => l.timestamp && l.timestamp.startsWith(fDate));

  const displayed = logs.slice(0, 200);

  const rows = displayed.map(l => `
    <tr>
      <td>${ist(l.timestamp)}</td>
      <td><code>${l.key || "—"}</code></td>
      <td><code>${l.ip || "—"}</code></td>
      <td>${l.endpoint || "—"}</td>
      <td>${l.number || "—"}</td>
      <td>${l.responseTime || 0}ms</td>
      <td><span class="badge badge-${l.status < 300 ? "active" : l.status < 500 ? "trial" : "suspended"}">${l.status}</span></td>
    </tr>`).join("");

  const body = `
    <div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;align-items:center">
      <a href="/ftadmin/logs/export" class="btn btn-ghost">↓ Export</a>
      <form method="POST" action="/ftadmin/logs/clear" onsubmit="return confirm('Clear all logs?')" style="display:inline">
        <button class="btn btn-danger">Clear Logs</button>
      </form>
      <span style="margin-left:auto;color:var(--muted);font-size:12px">Showing ${displayed.length} of ${logs.length}</span>
    </div>

    <div class="card">
      <form method="GET" style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap">
        <input name="key" value="${fKey || ""}" placeholder="Filter by key…" style="flex:1;min-width:140px">
        <input name="ip"  value="${fIP  || ""}" placeholder="Filter by IP…"  style="flex:1;min-width:120px">
        <input type="date" name="date" value="${fDate || ""}" style="width:140px">
        <button type="submit" class="btn btn-ghost">Filter</button>
        <a href="/ftadmin/logs" class="btn btn-ghost">Reset</a>
      </form>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Time (IST)</th><th>Key</th><th>IP</th><th>Endpoint</th><th>Number</th><th>Time</th><th>Status</th></tr></thead>
          <tbody>
            ${rows || `<tr><td colspan=7 style="color:var(--muted);text-align:center;padding:24px">No logs</td></tr>`}
          </tbody>
        </table>
      </div>
    </div>

    <script>setTimeout(() => location.reload(), 30000);</script>
  `;
  res.send(layout("Access Logs", body, "logs"));
});

router.get("/logs/export", requireAuth, (req, res) => {
  const logs = store.logs();
  const headers = ["timestamp","key","ip","endpoint","number","responseTime","status"];
  const csv = [
    headers.join(","),
    ...logs.map(l => headers.map(h => JSON.stringify(l[h] ?? "")).join(","))
  ].join("\n");
  res.setHeader("Content-Disposition", "attachment; filename=logs.csv");
  res.setHeader("Content-Type", "text/csv");
  res.send(csv);
});

router.post("/logs/clear", requireAuth, (req, res) => {
  const f = require("path").join(__dirname, "../data/logs.json");
  require("fs").writeFileSync(f, "[]");
  store.reloadLogs();
  res.redirect("/ftadmin/logs?msg=Logs cleared");
});

// ── Settings ───────────────────────────────────────────────────────────────────

router.get("/settings", requireAuth, (req, res) => {
  const settings = mw.loadSettings();
  const msg = req.query.msg || "";

  const body = `
    ${msg ? `<div class="alert alert-success">${msg}</div>` : ""}
    <div class="card">
      <div class="card-title">Auto-Block Settings</div>
      <form method="POST" action="/ftadmin/settings">
        <div class="form-grid">
          <div class="form-group">
            <label>Auto-Block Threshold (requests/min)</label>
            <input type="number" name="autoBlockThreshold" value="${settings.autoBlockThreshold || 200}" min="1">
          </div>
        </div>
        <div style="margin-top:16px">
          <button type="submit" class="btn btn-primary">Save Settings</button>
        </div>
      </form>
    </div>

    <div class="card" style="margin-top:20px">
      <div class="card-title">Backup</div>
      <p style="color:var(--muted);font-size:13px;margin-bottom:16px">Download a ZIP archive of all data files.</p>
      <a href="/ftadmin/backup/download" class="btn btn-ghost">↓ Download Backup</a>
    </div>

    <div class="card" style="margin-top:20px">
      <div class="card-title">Change Password</div>
      <form method="POST" action="/ftadmin/settings/password">
        <div class="form-grid">
          <div class="form-group">
            <label>Current Password</label>
            <input type="password" name="current" required>
          </div>
          <div class="form-group">
            <label>New Password</label>
            <input type="password" name="newPass" required minlength="8">
          </div>
          <div class="form-group">
            <label>Confirm New Password</label>
            <input type="password" name="confirm" required minlength="8">
          </div>
        </div>
        <div style="margin-top:16px">
          <button type="submit" class="btn btn-primary">Update Password</button>
        </div>
      </form>
    </div>
  `;
  res.send(layout("Settings", body, "settings"));
});

router.post("/settings", requireAuth, (req, res) => {
  const s = mw.loadSettings();
  s.autoBlockThreshold = parseInt(req.body.autoBlockThreshold) || 200;
  mw.saveSettings(s);
  res.redirect("/ftadmin/settings?msg=Settings saved");
});

router.post("/settings/password", requireAuth, (req, res) => {
  const { current, newPass, confirm } = req.body;
  const currentPass = process.env.ADMIN_PASSWORD || "Dilshan418@";
  if (current !== currentPass) return res.redirect("/ftadmin/settings?msg=Current password incorrect");
  if (newPass !== confirm) return res.redirect("/ftadmin/settings?msg=Passwords do not match");
  process.env.ADMIN_PASSWORD = newPass;
  res.redirect("/ftadmin/settings?msg=Password updated (restart server to persist)");
});

// ── Backup ─────────────────────────────────────────────────────────────────────

router.get("/backup/download", requireAuth, (req, res) => {
  res.setHeader("Content-Disposition", `attachment; filename=ftadmin-backup-${Date.now()}.zip`);
  res.setHeader("Content-Type", "application/zip");
  const archive = archiver("zip");
  archive.pipe(res);
  const dataDir = path.join(__dirname, "../data");
  ["keys.json","stats.json","logs.json","blocked.json","settings.json"].forEach(f => {
    const fp = path.join(dataDir, f);
    if (fs.existsSync(fp)) archive.file(fp, { name: f });
  });
  archive.finalize();
});

module.exports = router;
