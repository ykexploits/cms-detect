import requests
import sys
import os
import re
import json
import time
import random
import hashlib
import urllib3
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

R  = "\033[0m"
RD = "\033[38;5;196m"
RD2 = "\033[38;5;160m"
RD3 = "\033[38;5;124m"
RD4 = "\033[38;5;88m"
RD5 = "\033[38;5;52m"
GY = "\033[38;5;245m"
WH = "\033[38;5;255m"

ASCII_LINES = [
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢶⠼⢻⣷⣦⡀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⢃⠐⣏⣟⣸⢣⡆⠀⠀⠀⠐⠳⠃⠉⣥⣆⣠⣠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡷⠤⣬⠍⠉⠁⠆⠀⠀⠀⠨⢼⡄⠜⢿⣭⡼⠋⡦⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠋⠲⠆⠘⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣼⣿⣼⣿⣿⣤⣤⣀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠶⠖⠶⣶⣄⣄⡀⠀⠀⢺⡿⠟⠛⠋⠉⡻⣿⣿⣿⣿⡆",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⣿⡯⠿⠽⢆⠠⡀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠃⢰⣿⣷⠌⡿⢻⡃⠀⠀⢋⠀⠀⠀⠀⢰⣼⣤⣽⣿⡯⡇",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣟⢠⢾⣶⡄⢹⠼⢦⠀⠀⠀⠀⠀⠀⠀⠿⠒⡓⠊⠉⠁⡀⣴⡛⠋⠀⢀⠆⠀⠀⠀⠀⢸⣿⣿⣿⣛⣡⣧",
"⠀⠀⠀⠀⢀⢠⣠⣠⠀⡀⠀⠀⠀⢻⣌⠋⠛⠚⢁⡡⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠓⠋⠁⠁⠀⠀⠀⠠⣞⠠⣀⠀⠀⠀⠙⢿⣿⣿⣿⡇",
"⠀⢠⡴⣿⣿⡿⡄⠹⡑⡕⠀⠀⠀⠀⠛⠛⠒⠋⢉⣦⣦⣞⡢⢄⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⡇⠂⠠⠀⡤⠒⠂⠒⠂⠘",
"⠈⢭⡣⠳⢯⡵⠃⢠⠱⠼⠀⠀⠀⠀⠀⠀⠀⢠⡿⢹⣝⣻⠇⢸⢱⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀",
"⠀⠀⠉⠳⠜⠆⠁⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠚⠪⠅⠤⠘⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠝⢉⣡⣬⡐⠺⡂",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⠀⠠⠄⠤⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⣕⣀⢺⣟⣛⣷⣴⠈",
"⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠬⠀⢠⣾⡯⣷⠀⡳⡔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠉⠈⠀⠀",
"⠀⠀⠀⠾⣷⣾⠿⣛⣶⣟⡷⠦⣄⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠺⣻⣛⠛⠍⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠰⠰⣅⠀⣼⣟⣿⣿⠿⡆⠈⡹⣷⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⣥⣈⠁⠙⢬⣌⣭⡾⠃⠀⢹⣦⠷⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠧⠉⠛⠢⣄⣤⣠⡀⣠⣤⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣬⠿⠛⢉⣉⣛⡻⢮⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠾⢷⡁⠀⢰⡿⢫⣿⣿⡆⠈⢻⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⣀⡀⠀⣄⢠⡀⡀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠀⡉⠂⠘⢯⣼⣷⡿⠃⢀⠞⡙⠁⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣦⣼⡖⠓⣼⣼⢠⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⣵⣤⢠⠀⠀⢠⣤⠚⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣬⣿⠅⠀⠀⢀⠔⠚⣶⣾⡽⣞⣤⠠⡀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⣼⡿⣷⣾⣷⣆⠰⣿⡷⡀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠄⠀⠀⢹⡥⣌⠟⠛⠁⡜⣿⠀⢰⢎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠆⠀⠀⠀⠙⠾⣦⠶⣦⢞⡁⠀⠈⠸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
]

ASCII_COLORS = [RD5, RD4, RD3, RD2, RD, RD, RD2, RD3, RD4, RD5, RD5, RD4, RD3, RD2, RD, RD2, RD3, RD4, RD5, RD5, RD4, RD3, RD2, RD]

AUTHOR = "YkExploits"
VERSION = "1.2"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; DuckDuckBot/1.0; +http://duckduckgo.com/duckduckbot.html)",
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
]

SIGNATURES = {
    "wordpress": {
        "headers": ["x-pingback", "link: <https://api.w.org/"],
        "cookies": ["wordpress_", "wp-settings-", "wp_woocommerce_session_"],
        "meta": [r'<meta name="generator" content="WordPress'],
        "paths": ["/wp-content/", "/wp-includes/", "/wp-json/", "/xmlrpc.php", "/wp-login.php"],
        "html": [r'wp-content/themes/', r'wp-includes/js/'],
        "version_regex": r'<meta name="generator" content="WordPress ([\d.]+)"',
    },
    "joomla": {
        "headers": ["x-content-encoded-by: Joomla"],
        "cookies": ["joomla_", "jos_"],
        "meta": [r'<meta name="generator" content="Joomla'],
        "paths": ["/administrator/", "/components/com_", "/modules/mod_", "/plugins/", "/language/en-GB/en-GB.xml", "/administrator/manifests/files/joomla.xml"],
        "html": [r'option=com_content', r'/media/system/js/'],
        "version_regex": r'<version>([\d.]+)</version>',
    },
    "drupal": {
        "headers": ["x-drupal-cache", "x-generator: Drupal", "x-drupal-dynamic-cache"],
        "cookies": ["SESS", "SSESS"],
        "meta": [r'<meta name="generator" content="Drupal'],
        "paths": ["/sites/default/", "/core/", "/modules/", "/themes/", "/CHANGELOG.txt"],
        "html": [r'drupal.org', r'Drupal.settings'],
        "version_regex": r'<meta name="generator" content="Drupal ([\d.]+)"',
    },
    "magento": {
        "headers": ["x-magento-cache-debug", "x-magento-tags"],
        "cookies": ["frontend=", "adminhtml="],
        "meta": [r'<meta name="generator" content="Magento'],
        "paths": ["/media/", "/skin/", "/js/", "/downloader/", "/app/"],
        "html": [r'Magento', r'mage/cookies'],
        "version_regex": r'Magento/([\d.]+)',
    },
    "shopify": {
        "headers": ["x-shopid", "x-shopify-stage", "x-sorting-hat-shopid"],
        "cookies": ["_shopify_s", "_shopify_y"],
        "meta": [],
        "paths": ["/admin/", "/cart/", "/collections/"],
        "html": [r'cdn.shopify.com', r'Shopify.theme'],
        "version_regex": None,
    },
    "prestashop": {
        "headers": ["x-prestashop"],
        "cookies": ["PrestaShop-"],
        "meta": [r'<meta name="generator" content="PrestaShop'],
        "paths": ["/modules/", "/themes/", "/admin/"],
        "html": [r'var prestashop', r'prestashop.com'],
        "version_regex": r'<meta name="generator" content="PrestaShop ([\d.]+)"',
    },
    "opencart": {
        "headers": [],
        "cookies": ["OCSESSID"],
        "meta": [],
        "paths": ["/catalog/", "/admin/", "/system/"],
        "html": [r'index.php?route=', r'catalog/view/theme/'],
        "version_regex": None,
    },
    "wix": {
        "headers": ["x-wix-request-id", "x-wix-"],
        "cookies": ["XSRF-TOKEN", "wixSession"],
        "meta": [],
        "paths": [],
        "html": [r'wix.com', r'wixstatic.com', r'X-Wix-'],
        "version_regex": None,
    },
    "squarespace": {
        "headers": ["x-squarespace-"],
        "cookies": ["SS_"],
        "meta": [r'<meta name="generator" content="Squarespace'],
        "paths": [],
        "html": [r'squarespace.com', r'static1.squarespace.com'],
        "version_regex": None,
    },
    "ghost": {
        "headers": [],
        "cookies": [],
        "meta": [r'<meta name="generator" content="Ghost'],
        "paths": ["/ghost/", "/content/"],
        "html": [r'ghost.io', r'content/images/'],
        "version_regex": r'<meta name="generator" content="Ghost ([\d.]+)"',
    },
    "typo3": {
        "headers": [],
        "cookies": ["be_typo_user", "fe_typo_user"],
        "meta": [r'<meta name="generator" content="TYPO3'],
        "paths": ["/typo3/", "/typo3conf/", "/typo3temp/", "/fileadmin/"],
        "html": [r'typo3.org', r'typo3conf/'],
        "version_regex": r'<meta name="generator" content="TYPO3 ([\d.]+)"',
    },
    "laravel": {
        "headers": [],
        "cookies": ["laravel_session", "XSRF-TOKEN"],
        "meta": [],
        "paths": [],
        "html": [r'laravel', r'csrf-token'],
        "version_regex": None,
    },
    "django": {
        "headers": [],
        "cookies": ["csrftoken", "sessionid"],
        "meta": [],
        "paths": ["/admin/", "/static/"],
        "html": [r'csrfmiddlewaretoken', r'django'],
        "version_regex": None,
    },
    "rails": {
        "headers": ["x-runtime", "x-request-id"],
        "cookies": ["_session_id", "_rails_session"],
        "meta": [],
        "paths": [],
        "html": [r'csrf-param', r'csrf-token'],
        "version_regex": None,
    },
}

VERSION_PATHS = {
    "wordpress": ["/readme.html", "/wp-includes/version.php"],
    "joomla": ["/administrator/manifests/files/joomla.xml", "/language/en-GB/en-GB.xml"],
    "drupal": ["/CHANGELOG.txt", "/core/CHANGELOG.txt"],
    "magento": ["/magento_version", "/Magento_Version"],
}

PROXIES = []

def load_proxies(path="proxies.txt"):
    global PROXIES
    if os.path.exists(path):
        with open(path) as f:
            PROXIES = [l.strip() for l in f if l.strip()]
    return len(PROXIES)

def get_proxy():
    return random.choice(PROXIES) if PROXIES else None

def new_session():
    s = requests.Session()
    s.verify = False
    s.headers["User-Agent"] = random.choice(USER_AGENTS)
    proxy = get_proxy()
    if proxy:
        s.proxies = {"http": proxy, "https": proxy}
    return s

def banner():
    os.system("clear" if os.name == "posix" else "cls")
    for line, col in zip(ASCII_LINES, ASCII_COLORS):
        print(col + line + R)
    print()
    print(RD + "  cms-detect" + R + GY + " v" + VERSION + R)
    print(RD2 + "  by " + AUTHOR + R)
    print()

def fetch(url, session, timeout=12, allow_redirects=True):
    try:
        r = session.get(url, timeout=timeout, allow_redirects=allow_redirects)
        return r
    except requests.RequestException:
        return None

def analyze_headers(headers):
    h = {k.lower(): v for k, v in headers.items()}
    result = {}
    if "x-powered-by" in h:
        result["x-powered-by"] = h["x-powered-by"]
    if "server" in h:
        result["server"] = h["server"]
    if "x-generator" in h:
        result["x-generator"] = h["x-generator"]
    if "x-drupal-cache" in h:
        result["drupal"] = True
    if "x-magento-tags" in h:
        result["magento"] = True
    if "x-shopify-stage" in h:
        result["shopify"] = True
    if "x-pingback" in h:
        result["wordpress"] = True
    return result

def analyze_cookies(cookies):
    names = [c.name for c in cookies]
    result = {}
    for name in names:
        if "wordpress" in name.lower() or name.startswith("wp-"):
            result["wordpress"] = True
        if "joomla" in name.lower() or name.startswith("jos_"):
            result["joomla"] = True
        if name.startswith("SESS") or name.startswith("SSESS"):
            result["drupal"] = True
        if "frontend" in name.lower() or "adminhtml" in name.lower():
            result["magento"] = True
    return result

def analyze_html(html):
    result = {}
    for cms, sig in SIGNATURES.items():
        for pattern in sig.get("meta", []):
            if re.search(pattern, html, re.I):
                result[cms] = True
        for pattern in sig.get("html", []):
            if re.search(pattern, html, re.I):
                result[cms] = True
    return result

def check_paths(base_url, session, cms):
    sig = SIGNATURES.get(cms)
    if not sig:
        return False
    paths = sig.get("paths", [])
    for path in paths:
        url = urljoin(base_url, path)
        r = fetch(url, session, timeout=6, allow_redirects=False)
        if r and r.status_code in (200, 403, 401, 500):
            return True
    return False

def extract_version(base_url, session, cms):
    if cms in VERSION_PATHS:
        for path in VERSION_PATHS[cms]:
            url = urljoin(base_url, path)
            r = fetch(url, session, timeout=8)
            if r and r.status_code == 200:
                if cms == "wordpress":
                    m = re.search(r'Version ([\d.]+)', r.text)
                    if m:
                        return m.group(1)
                elif cms == "joomla":
                    m = re.search(r'<version>([\d.]+)</version>', r.text)
                    if m:
                        return m.group(1)
                elif cms == "drupal":
                    m = re.search(r'Drupal ([\d.]+)', r.text)
                    if m:
                        return m.group(1)
                elif cms == "magento":
                    m = re.search(r'Magento/([\d.]+)', r.text)
                    if m:
                        return m.group(1)
    sig = SIGNATURES.get(cms)
    if sig and sig.get("version_regex"):
        r = fetch(base_url, session, timeout=10)
        if r:
            m = re.search(sig["version_regex"], r.text, re.I)
            if m:
                return m.group(1)
    return None

def detect_cms(url):
    session = new_session()
    base = url.rstrip("/")
    if not base.startswith(("http://", "https://")):
        base = "https://" + base

    result = {
        "url": base,
        "cms": None,
        "version": None,
        "confidence": 0,
        "signals": [],
        "server": None,
        "x-powered-by": None,
    }

    r = fetch(base, session)
    if not r:
        return result

    headers = analyze_headers(r.headers)
    cookies = analyze_cookies(r.cookies)
    html = analyze_html(r.text)

    result["server"] = headers.get("server")
    result["x-powered-by"] = headers.get("x-powered-by")

    scores = {}
    for cms in SIGNATURES:
        score = 0
        if headers.get(cms):
            score += 3
            result["signals"].append(f"header:{cms}")
        if cookies.get(cms):
            score += 2
            result["signals"].append(f"cookie:{cms}")
        if html.get(cms):
            score += 2
            result["signals"].append(f"html:{cms}")
        if score > 0:
            scores[cms] = score

    for cms in scores:
        if check_paths(base, session, cms):
            scores[cms] += 2
            result["signals"].append(f"path:{cms}")

    if not scores:
        return result

    best = max(scores, key=scores.get)
    result["cms"] = best
    result["confidence"] = min(scores[best] * 10, 100)

    version = extract_version(base, session, best)
    if version:
        result["version"] = version

    return result

def crawl(base_url, max_pages=20, max_depth=2):
    session = new_session()
    base = base_url.rstrip("/")
    if not base.startswith(("http://", "https://")):
        base = "https://" + base

    seen = set()
    queue = [(base, 0)]
    found = []

    while queue and len(seen) < max_pages:
        url, depth = queue.pop(0)
        if url in seen or depth > max_depth:
            continue
        seen.add(url)
        r = fetch(url, session, timeout=8)
        if not r or r.status_code != 200:
            continue
        found.append(url)
        for link in re.findall(r'href=["\']([^"\']+)["\']', r.text):
            full = urljoin(base, link)
            if full.startswith(base) and full not in seen:
                queue.append((full, depth + 1))
    return found

def main():
    banner()
    load_proxies()

    if len(sys.argv) < 2:
        print(RD + "usage: python3 cms_detect.py <url> [--crawl]" + R)
        sys.exit(1)

    target = sys.argv[1]
    do_crawl = "--crawl" in sys.argv

    print(RD2 + "[*] target: " + target + R)
    if PROXIES:
        print(RD3 + "[*] proxies: " + str(len(PROXIES)) + R)

    result = detect_cms(target)

    print()
    print(RD + "  cms        : " + str(result["cms"]) + R)
    print(RD2 + "  version    : " + str(result["version"]) + R)
    print(RD3 + "  confidence : " + str(result["confidence"]) + "%" + R)
    print(RD4 + "  server     : " + str(result["server"]) + R)
    print(RD5 + "  x-powered  : " + str(result["x-powered-by"]) + R)
    if result["signals"]:
        print(GY + "  signals    : " + ", ".join(result["signals"]) + R)

    if do_crawl and result["cms"]:
        print()
        print(RD2 + "[*] crawling..." + R)
        pages = crawl(target, max_pages=15, max_depth=2)
        print(RD3 + "[*] pages found: " + str(len(pages)) + R)
        for p in pages[:10]:
            print(GY + "  " + p + R)

    with open("cms_result.json", "w") as f:
        json.dump(result, f, indent=2)
    print()
    print(RD + "[*] saved: cms_result.json" + R)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(RD + "\n[!] interrupted." + R)
        sys.exit(0)
