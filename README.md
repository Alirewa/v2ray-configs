# 🔒 Free V2Ray Configs — Auto-Updated Every 30 Minutes

> **Free, fresh, and ready-to-use V2Ray subscription links** — updated automatically
> every 30 minutes from 180+ Telegram channels and verified GitHub sources.
> Pure raw output — compatible with any V2Ray client or Telegram bot.

---

## ⚡ Subscription Link

```
https://raw.githubusercontent.com/Alirewa/v2ray-configs/main/config.txt
```

> One config per line. No headers. Directly usable as a subscription URL.

---

## 📊 Stats

| Item | Value |
|------|-------|
| 🔄 Update interval | Every 30 minutes |
| 📡 Sources | 180+ Telegram channels + 20 GitHub repos |
| 🔢 Max configs | 2,000 (after full deduplication) |
| 🧹 Dedup method | Exact string + UUID/identifier matching |
| 📄 Output format | Raw — one config per line |
| 🆓 Cost | Free forever (GitHub Actions) |

---

## 📋 Supported Protocols

| Protocol | Format |
|----------|--------|
| VLESS | `vless://UUID@host:port?...#name` |
| VMess | `vmess://base64encodedJSON#name` |
| Trojan | `trojan://password@host:port#name` |
| Shadowsocks | `ss://base64@host:port#name` |

---

## 📱 How to Use

### Android — V2RayNG
1. Open V2RayNG → **☰** → **Subscription group settings**
2. Tap **+** → paste the URL above → Save
3. **☰** → **Update subscription** → connect

### iOS — Shadowrocket
1. Tap **+** → Type: **Subscribe**
2. Paste URL → Save → **Update**

### Windows — V2RayN / Hiddify
1. **Subscriptions** → **Add subscription URL**
2. Paste → OK → **Update subscriptions**

### Telegram Bot Integration
Use the raw URL directly as a subscription source in your bot.
The file contains one config per line with no headers — standard format.

```
https://raw.githubusercontent.com/Alirewa/v2ray-configs/main/config.txt
```

### CLI / curl
```bash
curl -s https://raw.githubusercontent.com/Alirewa/v2ray-configs/main/config.txt | head -20
```

---

## 🔄 How It Works

```
Every 30 min — GitHub Actions (free)
        │
        ├── Scrape 180+ Telegram channels (t.me/s/...)
        │         └── parse <code> tags for v2ray configs
        │
        ├── Fetch 20 GitHub aggregator repos (raw .txt files)
        │         └── decode base64 if needed
        │
        ├── Deduplication
        │         ├── Pass 1: exact string match
        │         └── Pass 2: UUID / identifier match
        │
        ├── Cap at 2,000 configs
        │
        └── Write config.txt → auto-commit → push
```

---

## 🔍 Search Keywords

`v2ray config` · `free v2ray subscription` · `vless config free` · `vmess config`
`trojan config free` · `v2ray sub link` · `shadowsocks config` · `v2rayNG subscription`
`free vpn config 2026` · `v2ray subscription url` · `xray config` · `free proxy config`
`کانفیگ رایگان` · `سابسکریپشن v2ray` · `کانفیگ vless` · `لینک سابسکریپشن`

---

## ⚠️ Disclaimer

Configs are collected from **publicly available** Telegram channels and GitHub repositories.
Use responsibly and in accordance with your local laws.

---

⭐ Star the repo if it helped you!
