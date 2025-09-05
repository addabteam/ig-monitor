import os, requests, json, pathlib

TG_TOKEN = os.environ["TG_TOKEN"]
TG_CHAT_ID = os.environ["TG_CHAT_ID"]
USERNAMES = [u.strip() for u in os.environ.get("USERNAMES","").split(",") if u.strip()]

STATE_FILE = pathlib.Path("state.json")
state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}

def is_active(username: str) -> bool:
    url = f"https://www.instagram.com/{username}/"
    headers = {"User-Agent":"Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        return r.status_code == 200
    except Exception:
        return False

def send_tg(text: str):
    requests.post(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        json={"chat_id": TG_CHAT_ID, "text": text, "parse_mode":"HTML"},
        timeout=15
    )

changed = []
for u in USERNAMES:
    now_active = is_active(u)
    was_active = bool(state.get(u, False))
    if now_active and not was_active:
        changed.append(f"✅ الحساب رجع Live — @{u}\\nhttps://www.instagram.com/{u}/")
    state[u] = now_active

if changed:
    send_tg("\\n\\n".join(changed))

STATE_FILE.write_text(json.dumps(state, indent=2))
