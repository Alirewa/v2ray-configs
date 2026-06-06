"""
V2Ray Config Aggregator
Fetches vmess/vless/ss/trojan configs from:
  - 180+ public Telegram channel web-previews
  - Top GitHub aggregator repos (raw subscription files)
Deduplicates and writes to config.txt every 15 minutes via GitHub Actions.
"""

import base64
import json
import re
import requests
from bs4 import BeautifulSoup
import pytz
import jdatetime

# ── Constants ────────────────────────────────────────────────────────────────

SCHEMES = ("vmess://", "vless://", "ss://", "trojan://")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# ── Telegram Sources (public web-preview pages) ───────────────────────────────

TELEGRAM_SOURCES = [
    "https://t.me/s/Awlix_ir",
    "https://t.me/s/beiten",
    "https://t.me/s/beta_v2ray",
    "https://t.me/s/CloudCityy",
    "https://t.me/s/config_v2ray",
    "https://t.me/s/Configforvpn01",
    "https://t.me/s/ConfigsHubPlus",
    "https://t.me/s/configV2rayForFree",
    "https://t.me/s/configV2rayNG",
    "https://t.me/s/DailyV2RY",
    "https://t.me/s/DigiV2ray",
    "https://t.me/s/DirectVPN",
    "https://t.me/s/Easy_Free_VPN",
    "https://t.me/s/EliV2ray",
    "https://t.me/s/FalconPolV2rayNG",
    "https://t.me/s/forwardv2ray",
    "https://t.me/s/FOX_VPN66",
    "https://t.me/s/foxrayiran",
    "https://t.me/s/free4allVPN",
    "https://t.me/s/freeland8",
    "https://t.me/s/FreeNet1500",
    "https://t.me/s/FreeV2rays",
    "https://t.me/s/freev2rayssr",
    "https://t.me/s/FreeVlessVpn",
    "https://t.me/s/frev2ray",
    "https://t.me/s/frev2rayng",
    "https://t.me/s/God_CONFIG",
    "https://t.me/s/inikotesla",
    "https://t.me/s/iranvpnet",
    "https://t.me/s/iSeqaro",
    "https://t.me/s/mahsaamoon1",
    "https://t.me/s/MsV2ray",
    "https://t.me/s/napsternetv_config",
    "https://t.me/s/Network_442",
    "https://t.me/s/OutlineVpnOfficial",
    "https://t.me/s/ParsRoute",
    "https://t.me/s/PrivateVPNs",
    "https://t.me/s/proxystore11",
    "https://t.me/s/ServerNett",
    "https://t.me/s/Shadowlinkserverr",
    "https://t.me/s/ShadowSocks_s",
    "https://t.me/s/ShadowsocksM",
    "https://t.me/s/shadowsocksshop",
    "https://t.me/s/v2_team",
    "https://t.me/s/v2_vmess",
    "https://t.me/s/v2line",
    "https://t.me/s/V2pedia",
    "https://t.me/s/v2ray_ar",
    "https://t.me/s/v2ray_custom",
    "https://t.me/s/v2ray_for_free",
    "https://t.me/s/V2Ray_FreedomIran",
    "https://t.me/s/V2RAY_NEW",
    "https://t.me/s/v2ray_outlineir",
    "https://t.me/s/v2rayan",
    "https://t.me/s/v2RayChannel",
    "https://t.me/s/V2rayN_Free",
    "https://t.me/s/v2rayn_server",
    "https://t.me/s/v2rayng_org",
    "https://t.me/s/v2rayng_v",
    "https://t.me/s/v2rayNG_VPN",
    "https://t.me/s/V2RayOxygen",
    "https://t.me/s/ViPVpn_v2ray",
    "https://t.me/s/vmess_iran",
    "https://t.me/s/vmess_vless_v2rayng",
    "https://t.me/s/vmessiran",
    "https://t.me/s/VmessProtocol",
    "https://t.me/s/vmessq",
    "https://t.me/s/VorTexIRN",
    "https://t.me/s/VPN_443",
    "https://t.me/s/vpn_ocean",
    "https://t.me/s/vpn_proxy_custom",
    "https://t.me/s/vpn_tehran",
    "https://t.me/s/vpnmasi",
    "https://t.me/s/WeePeeN",
    "https://t.me/s/yaney_01",
    "https://t.me/s/YtTe3la",
    "https://t.me/s/vpn_xw",
    "https://t.me/s/azadi_az_inja_migzare",
    "https://t.me/s/reality_daily",
    "https://t.me/s/zen_cloud",
    "https://t.me/s/V2rayCollectorDonate",
    "https://t.me/s/iP_CF",
    "https://t.me/s/TLS_v2ray",
    "https://t.me/s/v2raycollector",
    "https://t.me/s/Cov2ray",
    "https://t.me/s/v2ray_cartel",
    "https://t.me/s/speedconfig00",
    "https://t.me/s/FOXNT",
    "https://t.me/s/EspinasVPN",
    "https://t.me/s/vpnsshocean",
    "https://t.me/s/filterkoshi",
    "https://t.me/s/ARv2ray",
    "https://t.me/s/Eleven_vpn",
    "https://t.me/s/freeownvpn",
    "https://t.me/s/msv2raynp",
    "https://t.me/s/Injastvpn",
    "https://t.me/s/Joker_v2ray_configs",
    "https://t.me/s/JOKERRVPN",
    "https://t.me/s/kvetch_matin",
    "https://t.me/s/mrsoulb",
    "https://t.me/s/Netifyvpn",
    "https://t.me/s/NETMelliAnti",
    "https://t.me/s/networld_vpn",
    "https://t.me/s/Prime_Verse",
    "https://t.me/s/SAVTEAM",
    "https://t.me/s/Shadownet021",
    "https://t.me/s/V2ray_Collector",
    "https://t.me/s/v2ray_hubb",
    "https://t.me/s/v2rayconfigsNN",
    "https://t.me/s/v2rayng_021",
    "https://t.me/s/V2RayNG_CaFe",
    "https://t.me/s/V2rayNG3",
    "https://t.me/s/v2rayserverfreenet",
    "https://t.me/s/v2xay",
    "https://t.me/s/vemssprotocol",
    "https://t.me/s/vpnaloo",
    "https://t.me/s/zeshtobad",
    "https://t.me/s/ProxyFn",
    "https://t.me/s/prrofile_purple",
    "https://t.me/s/shadowproxy66",
    "https://t.me/s/sinavm",
    "https://t.me/s/VPNCUSTOMIZE",
    "https://t.me/s/Outline_ir",
    "https://t.me/s/Pruoxyi",
    "https://t.me/s/v2ray_configs_pool",
    "https://t.me/s/v2ray_configs_pools",
    "https://t.me/s/ultrasurf_12",
    "https://t.me/s/V2RAY_VMESS_free",
    "https://t.me/s/FreakConfig",
    "https://t.me/s/v2rayNG_Matsuri",
    "https://t.me/s/meli_proxyy",
    "https://t.me/s/oneclickvpnkeys",
    "https://t.me/s/Outline_Vpn",
    "https://t.me/s/proxy_kafee",
    "https://t.me/s/v2ray_sub",
    "https://t.me/s/SaghiVpnX",
    "https://t.me/s/Daily_Configs",
    "https://t.me/s/customv2ray",
    "https://t.me/s/UnlimitedDev",
    "https://t.me/s/vmessorg",
    "https://t.me/s/v2rayngvpn",
    "https://t.me/s/SafeNet_Server",
    "https://t.me/s/vmesskhodam",
    "https://t.me/s/singbox1",
    "https://t.me/s/Viturey",
    "https://t.me/s/pPal03",
    "https://t.me/s/Rayan_Config",
    "https://t.me/s/info_2it_channel",
    "https://t.me/s/lexernet",
    "https://t.me/s/AblNet7",
    "https://t.me/s/manzariyeh_rasht",
    # ── New additions ──────────────────────────────────────────────────────────
    "https://t.me/s/free_v2rayyy",
    "https://t.me/s/v2ray_free_conf",
    "https://t.me/s/V2RayFreeConfig",
    "https://t.me/s/VPN_Beast",
    "https://t.me/s/vpn_alex",
    "https://t.me/s/xray_config",
    "https://t.me/s/xrayconfigs",
    "https://t.me/s/HiN_VPN",
    "https://t.me/s/VmessVpn",
    "https://t.me/s/FreeV2rayConfigs",
    "https://t.me/s/v2rayng_config",
    "https://t.me/s/iranv2ray",
    "https://t.me/s/v2rayiranserver",
    "https://t.me/s/free_proxy_configs",
    "https://t.me/s/Freev2ray_ir",
    "https://t.me/s/v2ray_everyday",
    "https://t.me/s/VPN_Free_Pro",
    "https://t.me/s/VpnProSub",
    "https://t.me/s/TrojanVpnConfig",
    "https://t.me/s/trojanconfigs",
    "https://t.me/s/ShadowsocksConfig",
    "https://t.me/s/v2ray_iran",
    "https://t.me/s/configs_v2ray",
    "https://t.me/s/FREE_V2RAY_CONFIG",
    "https://t.me/s/FreeVPN_io",
    "https://t.me/s/IranianVpn",
    "https://t.me/s/OutlineConfig",
    "https://t.me/s/VPNHouse",
    "https://t.me/s/custom_configs",
    "https://t.me/s/frv2ray",
    "https://t.me/s/V2rayFreeServer",
]

# ── GitHub Raw Sources (plain-text subscription files, one config per line) ───

GITHUB_SOURCES = [
    # barry-far — large daily aggregator
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub2.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub3.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub4.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub5.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub6.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub7.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub8.txt",
    # mahdibland — confirmed working paths
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/splitted/vmess.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/splitted/trojan.txt",
    # freefq / free
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    # Pawdroid
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    # peasoft — NoMoreWalls
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",
    # ermaozi
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    # Surfboardv2ray
    "https://raw.githubusercontent.com/Surfboardv2ray/v2ray-worker-sub/master/Eternity",
    # Barabama
    "https://raw.githubusercontent.com/Barabama/FreeNodes/master/nodes/merged.txt",
    # resasanian — Mirza
    "https://raw.githubusercontent.com/resasanian/Mirza/main/best",
    # ALIILAPRO
    "https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/main/server.txt",
    # soroushmirzaei — configs collector (correct path)
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/channels/protocols/vless",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/channels/protocols/vmess",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/channels/protocols/trojan",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/channels/protocols/shadowsocks",
    # coldwater — daily configs
    "https://raw.githubusercontent.com/coldwater-10/V2Hub/main/split/vless",
    "https://raw.githubusercontent.com/coldwater-10/V2Hub/main/split/vmess",
    "https://raw.githubusercontent.com/coldwater-10/V2Hub/main/split/trojan",
    # Epodonios
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
    # yebekhe — TelegramV2rayCollector
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix",
    # mahdibland SplitV2Ray
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity.txt",
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def _get(url: str) -> str:
    """Fetch a URL; return empty string on any error."""
    try:
        r = requests.get(url.strip(), headers=HEADERS, timeout=20)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"  [SKIP] {url.split('/')[-1][:40]} — {e}")
        return ""


def _clean(line: str) -> str:
    """Strip the #comment fragment and surrounding whitespace."""
    return line.split("#")[0].rstrip()


def _is_valid(cfg: str) -> bool:
    """Basic sanity check — must start with a known scheme and have some length."""
    return any(cfg.startswith(s) for s in SCHEMES) and len(cfg) > 20


def _extract_uuid(cfg: str) -> str | None:
    """
    Extract the unique identifier from a config string:
      vless / trojan  → the token before the first '@'
      vmess           → the "id" field inside the base64-decoded JSON
      ss              → method:password (decoded if base64-encoded)
    Returns None when extraction fails.
    """
    try:
        scheme, rest = cfg.split("://", 1)

        if scheme in ("vless", "trojan"):
            # vless://UUID@host:port?...
            uid = rest.split("@")[0].strip()
            return uid.lower() if uid else None

        elif scheme == "vmess":
            # vmess://base64(JSON)
            b64 = rest.split("#")[0].strip()
            # pad to multiple of 4
            b64 += "=" * (-len(b64) % 4)
            data = json.loads(base64.b64decode(b64).decode("utf-8", errors="ignore"))
            uid = str(data.get("id", "")).strip()
            return uid.lower() if uid else None

        elif scheme == "ss":
            # two forms:
            #   ss://BASE64(method:password)@host:port
            #   ss://method:password@host:port   (SIP002)
            user_info = rest.split("@")[0].strip()
            # try base64 decode
            try:
                padded = user_info + "=" * (-len(user_info) % 4)
                decoded = base64.b64decode(padded).decode("utf-8", errors="ignore")
                if ":" in decoded:
                    return decoded.lower()
            except Exception:
                pass
            return user_info.lower() if ":" in user_info else None

    except Exception:
        return None


# ── Scrapers ──────────────────────────────────────────────────────────────────

def scrape_telegram(url: str) -> list[str]:
    """Parse <code> blocks from a Telegram web-preview page."""
    html = _get(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for tag in soup.find_all("code"):
        for raw_line in tag.get_text(separator="\n").splitlines():
            line = raw_line.strip()
            if any(line.startswith(s) for s in SCHEMES):
                cfg = _clean(line)
                if _is_valid(cfg):
                    results.append(cfg)
    return results


def fetch_raw(url: str) -> list[str]:
    """
    Parse a plain-text subscription file.
    Handles both raw-per-line files and base64-encoded subscription blobs.
    """
    text = _get(url)
    if not text:
        return []

    # Try base64 decode first (common subscription format)
    stripped = text.strip()
    if not any(stripped.startswith(s) for s in SCHEMES):
        try:
            import base64
            decoded = base64.b64decode(stripped + "==").decode("utf-8", errors="ignore")
            if any(decoded.startswith(s) for s in SCHEMES) or any(f"\n{s}" in decoded for s in SCHEMES):
                text = decoded
        except Exception:
            pass  # not base64, treat as plain text

    results = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if any(line.startswith(s) for s in SCHEMES):
            cfg = _clean(line)
            if _is_valid(cfg):
                results.append(cfg)
    return results


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    all_configs: list[str] = []

    print(f"\n{'='*55}")
    print(f" Fetching from {len(TELEGRAM_SOURCES)} Telegram channels...")
    print(f"{'='*55}")
    tg_total = 0
    for url in TELEGRAM_SOURCES:
        found = scrape_telegram(url)
        if found:
            tg_total += len(found)
            all_configs.extend(found)
            print(f"  ✓ {url.split('/')[-1]:35s} {len(found):>4} configs")

    print(f"\n{'='*55}")
    print(f" Fetching from {len(GITHUB_SOURCES)} GitHub sources...")
    print(f"{'='*55}")
    gh_total = 0
    for url in GITHUB_SOURCES:
        found = fetch_raw(url)
        if found:
            gh_total += len(found)
            all_configs.extend(found)
            label = "/".join(url.split("/")[3:5])
            print(f"  ✓ {label:35s} {len(found):>5} configs")

    # ── Deduplicate ───────────────────────────────────────────────────────────
    # Pass 1: exact string dedup (preserves first-seen order)
    seen_raw: set[str] = set()
    after_raw: list[str] = []
    for cfg in all_configs:
        if cfg not in seen_raw:
            seen_raw.add(cfg)
            after_raw.append(cfg)

    # Pass 2: UUID / identifier dedup
    # If two configs share the same UUID, keep only the first one.
    seen_uuid: set[str] = set()
    unique: list[str] = []
    uuid_dupes = 0
    for cfg in after_raw:
        uid = _extract_uuid(cfg)
        if uid:
            if uid in seen_uuid:
                uuid_dupes += 1
                continue          # duplicate UUID → skip
            seen_uuid.add(uid)
        unique.append(cfg)

    # ── Timestamp ─────────────────────────────────────────────────────────────
    now = jdatetime.datetime.now(pytz.timezone("Asia/Tehran"))
    date_str = now.strftime("%Y/%m/%d")
    time_str = now.strftime("%H:%M")

    # ── Write output ──────────────────────────────────────────────────────────
    header = (
        f"# ✅ به‌روزرسانی: {date_str} ساعت {time_str} | {len(unique)} کانفیگ یکتا\n"
        f"# 📡 منابع: {len(TELEGRAM_SOURCES)} کانال تلگرام + {len(GITHUB_SOURCES)} ریپوی گیتهاب\n"
        f"# 🔗 سابسکریپشن: https://raw.githubusercontent.com/Alirewa/v2ray-configs/main/config.txt\n"
    )

    with open("config.txt", "w", encoding="utf-8") as f:
        f.write(header)
        for i, cfg in enumerate(unique, start=1):
            label = f"#@Alirewa - #{i}"
            f.write(f"{cfg}{label}\n")

    print(f"\n{'='*55}")
    print(f" ✅ Done!")
    print(f"    Telegram      : {tg_total:>6} raw")
    print(f"    GitHub        : {gh_total:>6} raw")
    print(f"    Total raw     : {len(all_configs):>6}")
    print(f"    After str-dedup: {len(after_raw):>5}")
    print(f"    UUID dupes    : {uuid_dupes:>6}")
    print(f"    Final unique  : {len(unique):>6}  → saved to config.txt")
    print(f"    Total raw : {len(all_configs):>6}")
    print(f"    Unique    : {len(unique):>6}  →  saved to config.txt")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
