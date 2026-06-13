╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           CONTRIBUTING TO IG-PHISH                                ║
║           ⚡ We Build, We Break ⚡                                 ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝


<br>

![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge)

</div>

---

Thanks for wanting to contribute. Here\'s how we work.

---

## 🔄 Contribution Workflow

1. **Fork** the repository
2. **Create a feature branch** from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** — follow the code style below
4. **Test locally** — run `python app.py` and verify everything works
5. **Commit** with clear, descriptive messages
   ```bash
   git commit -m "feat: add SMS intercept module"
   ```
6. **Push** to your fork
7. **Open a Pull Request** — describe what you changed and why

---

## 📐 Code Style

### Python
- **PEP 8** compliance — use `black` formatter
- **Type hints** encouraged but not required
- **Docstrings** for all classes and public methods
- **Max line length:** 120 characters
- **Naming:** `snake_case` for variables/functions, `PascalCase` for classes, `UPPER_SNAKE` for constants

### Commit Messages
Follow conventional commits:

| Type | Use For |
|---|---|
| `feat:` | New features |
| `fix:` | Bug fixes |
| `refactor:` | Code restructure without behavior change |
| `docs:` | Documentation updates |
| `style:` | Formatting, whitespace (no logic change) |
| `chore:` | Build, CI, dependency updates |
| `perf:` | Performance improvements |

Examples:
```
feat: add EvilGinx2 integration for 2FA bypass
fix: resolve template path error on Windows
docs: update deployment guide for DigitalOcean
refactor: extract scanner detection into separate module
```

---

## 🎯 Priority Areas

We especially welcome contributions in these areas:

- **New Page Templates** — Facebook, Twitter, TikTok, banking portals
- **Anti-Detection Improvements** — Updated scanner signatures, new fingerprint evasion
- **Exfiltration Channels** — Telegram bot, Slack webhook, custom API endpoints
- **Docker Support** — Dockerfile + docker-compose for one-command deployment
- **Auto-SSL** — Let\'s Encrypt integration for custom domains
- **Analytics Dashboard** — Charts, conversion rates, geographic heatmaps
- **Mobile Optimization** — Better responsive design for the cloned pages
- **Rate Limiting** — Prevent brute-force detection by throttling requests

---

## 🧪 Testing

Before submitting a PR:

1. Run the server locally
2. Load the page in an incognito browser
3. Submit test credentials
4. Verify they appear in `/admin/creds`
5. Verify Discord webhook fires (if configured)
6. Check that scanner User-Agents get redirected (use a browser extension to spoof UA)
7. Confirm honeypot paths redirect properly

---

## 🚫 What Not To Do

- Don\'t commit `.env` files or real credentials
- Don\'t remove anti-detection features without discussion first
- Don\'t submit breaking changes without documenting migration steps
- Don\'t add dependencies without justification
- Don\'t refactor core architecture without opening an issue first

---

## 🐛 Bug Reports

Open a GitHub issue with:

- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Environment** (OS, Python version, deployment method)
- **Logs** (redact sensitive info)

---

## 💡 Feature Requests

Open a GitHub issue with the `enhancement` label. Include:

- **Use case** — What problem does this solve?
- **Proposed implementation** — How should it work?
- **Alternatives considered** — What else did you think about?

---

<div align="center">

*Good code is like a good con — clean, efficient, and nobody sees it coming.*

</div>