import streamlit as st
import random
import json
import os

# --- Your existing constants and CSS (omitted here for brevity) ---

LEADERBOARD_FILE = "leaderboard.json"

# --- Leaderboard functions ---

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    else:
        return []

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_leaderboard(name, crypto, passwords):
    leaderboard = load_leaderboard()
    found = False
    for entry in leaderboard:
        if entry["name"] == name:
            found = True
            if crypto > entry["max_crypto"]:
                entry["max_crypto"] = crypto
            if passwords > entry["max_passwords"]:
                entry["max_passwords"] = passwords
            break
    if not found:
        leaderboard.append({
            "name": name,
            "max_crypto": crypto,
            "max_passwords": passwords
        })
    leaderboard.sort(key=lambda x: (x["max_crypto"], x["max_passwords"]), reverse=True)
    leaderboard = leaderboard[:10]
    save_leaderboard(leaderboard)

def display_leaderboard():
    leaderboard = load_leaderboard()
    if not leaderboard:
        st.write("Leaderboard is empty.")
        return
    st.markdown("### 🏆 Leaderboard: Top Hackers 🏆")
    st.write("| Rank | Name | Max Crypto | Max Passwords |")
    st.write("| --- | --- | --- | --- |")
    for idx, entry in enumerate(leaderboard, start=1):
        st.write(f"| {idx} | {entry['name']} | {entry['max_crypto']} | {entry['max_passwords']} |")

# --- Initialization of session state variables ---

def init_state():
    defaults = {
        "crypto": 0,
        "passwords": 0,
        "crypto_per_click": 1,
        "password_drop_chance": 0.05,
        "upgrades": {
            "crypto_click": 0,
            "password_drop": 0,
            "bypass_firewall": 0,
            "decrypt_algorithms": 0,
            "quantum_decryptor": 0,
            "ai_botnet": 0,
        },
        "xp": 0,
        "xp_needed": 100,
        "level": 1,
        "minigame1_unlocked": False,
        "minigame2_unlocked": False,
        "max_level": 10,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

# --- Level up logic ---

def maybe_level_up():
    while st.session_state.xp >= st.session_state.xp_needed and st.session_state.level < st.session_state.max_level:
        st.session_state.xp -= st.session_state.xp_needed
        st.session_state.level += 1
        st.session_state.xp_needed = int(st.session_state.xp_needed * 1.5)
        st.success(f"🎉 Hacker Level UP! You are now Level {st.session_state.level}")

        if st.session_state.level >= 5:
            st.session_state.minigame1_unlocked = True
        if st.session_state.level >= 8:
            st.session_state.minigame2_unlocked = True

# --- Upgrade helpers and costs ---

upgrade_names = {
    "crypto_click": "Increase Crypto per Click",
    "password_drop": "Increase Password Drop Rate",
    "bypass_firewall": "Bypass Firewall (+10 Crypto/Click)",
    "decrypt_algorithms": "Decrypt Algorithms (+25 Crypto/Click +5% Password Drop)",
    "quantum_decryptor": "Quantum Decryptor (+70 Crypto/Click +7% Password Drop)",
    "ai_botnet": "AI-powered Botnet (+150 Crypto/Click +10% Password Drop)",
}

def upgrade_crypto_click():
    st.session_state.crypto_per_click += 1

def upgrade_password_drop():
    st.session_state.password_drop_chance = min(st.session_state.password_drop_chance + 0.02, 0.5)

def upgrade_bypass_firewall():
    st.session_state.crypto_per_click += 10

def upgrade_decrypt_algorithms():
    st.session_state.crypto_per_click += 25
    st.session_state.password_drop_chance = min(st.session_state.password_drop_chance + 0.05, 0.5)

def upgrade_quantum_decryptor():
    st.session_state.crypto_per_click += 70
    st.session_state.password_drop_chance = min(st.session_state.password_drop_chance + 0.07, 0.5)

def upgrade_ai_botnet():
    st.session_state.crypto_per_click += 150
    st.session_state.password_drop_chance = min(st.session_state.password_drop_chance + 0.1, 0.5)

upgrade_effects = {
    "crypto_click": upgrade_crypto_click,
    "password_drop": upgrade_password_drop,
    "bypass_firewall": upgrade_bypass_firewall,
    "decrypt_algorithms": upgrade_decrypt_algorithms,
    "quantum_decryptor": upgrade_quantum_decryptor,
    "ai_botnet": upgrade_ai_botnet,
}

def buy_upgrade(name):
    costs = {
        "crypto_click": (50, 0),
        "password_drop": (100, 1),
        "bypass_firewall": (500, 5),
        "decrypt_algorithms": (1200, 8),
        "quantum_decryptor": (3000, 15),
        "ai_botnet": (7000, 30),
    }
    level = st.session_state.upgrades[name]
    cost_crypto, cost_passwords = costs[name]
    cost_crypto = int(cost_crypto * (1.8 ** level))
    cost_passwords = int(cost_passwords * (1.6 ** level)) if cost_passwords > 0 else 0

    if st.session_state.crypto >= cost_crypto and st.session_state.passwords >= cost_passwords:
        st.session_state.crypto -= cost_crypto
        st.session_state.passwords -= cost_passwords
        upgrade_effects[name]()
        st.session_state.upgrades[name] += 1
        st.success(f"Upgrade bought: {upgrade_names[name]} (Level {st.session_state.upgrades[name]})")
    else:
        st.error(f"Not enough resources! Need {cost_crypto} Crypto and {cost_passwords} Passwords.")

# --- XP bar and stats ---

def draw_xp_bar():
    xp_percent = int((st.session_state.xp / st.session_state.xp_needed) * 100)
    bar_html = f"""
    <div style="position: relative; background-color: #003300; border: 1px solid #00ff00; border-radius: 5px; width: 100%; height: 25px; margin-bottom: 15px;">
      <div style="background: linear-gradient(90deg, #00ff00, #00cc00); height: 100%; border-radius: 5px; width: {xp_percent}%; transition: width 0.4s ease;"></div>
      <div style="position: absolute; width: 100%; text-align: center; top: 0; left: 0; color: black; font-weight: bold; line-height: 25px; font-family: 'Courier New', Courier, monospace;">
        Level {st.session_state.level} — XP: {st.session_state.xp} / {st.session_state.xp_needed} ({xp_percent}%)
      </div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)

def show_stats():
    stats = f"""
Crypto              : {st.session_state.crypto}
Passwords           : {st.session_state.passwords}
Crypto per Click    : {st.session_state.crypto_per_click}
Password Drop Chance: {int(st.session_state.password_drop_chance * 100)}%
Hacker Level        : {st.session_state.level}
"""
    st.markdown(f'<div style="font-family: \'Courier New\', monospace; font-size: 18px; background-color: #001a00; border: 1px solid #00ff00; padding: 10px; box-shadow: 0 0 6px #00ff00; margin-bottom: 15px; border-radius: 5px; white-space: pre;">{stats}</div>', unsafe_allow_html=True)
    draw_xp_bar()

# --- The core click function, also updates leaderboard ---

def game_update():
    update_leaderboard(
        st.session_state.player_name,
        st.session_state.crypto,
        st.session_state.passwords
    )

def click_crypto():
    st.session_state.crypto += st.session_state.crypto_per_click
    st.session_state.xp += 5
    maybe_level_up()
    if random.random() < st.session_state.password_drop_chance:
        st.session_state.passwords += 1
        st.toast("Password Cracked! +1 Password 🎁")
    game_update()

# --- Upgrades UI ---

def show_upgrades():
    st.header("Upgrades")
    for key, display_name in upgrade_names.items():
        lvl = st.session_state.upgrades[key]
        base_cost_crypto, base_cost_passwords = {
            "crypto_click": (50, 0),
            "password_drop": (100, 1),
            "bypass_firewall": (500, 5),
            "decrypt_algorithms": (1200, 8),
            "quantum_decryptor": (3000, 15),
            "ai_botnet": (7000, 30),
        }[key]
        cost_crypto = int(base_cost_crypto * (1.8 ** lvl))
        cost_passwords = int(base_cost_passwords * (1.6 ** lvl)) if base_cost_passwords > 0 else 0

        st.markdown(f"**{display_name}** (Level {lvl})  \nCost: {cost_crypto} Crypto{(' + ' + str(cost_passwords) + ' Password(s)') if cost_passwords > 0 else ''}")

        if st.button(f"Buy", key=f"buy_{key}"):
            buy_upgrade(key)

# --- Mod Menu omitted for brevity ---

# --- Minigames omitted for brevity ---

# --- Now handle player name input with hiding input on submission ---

if "player_name" not in st.session_state:
    st.session_state.player_name = ""

if st.session_state.player_name == "":
    name = st.text_input("Enter your hacker handle (name):")
    if name:
        st.session_state.player_name = name
        st.experimental_rerun()
    st.stop()

else:
    st.success(f"Welcome, {st.session_state.player_name}! Let's start hacking!")

# --- Main UI ---

st.title("🕵️‍♂️ Hacker Clicker: Crypto vs Firewall 🪙")

show_stats()

st.markdown("<hr>", unsafe_allow_html=True)

if st.button("🪙 Hack Crypto"):
    click_crypto()

st.markdown("<hr>", unsafe_allow_html=True)

show_upgrades()

st.markdown("<hr>", unsafe_allow_html=True)

# Mod menu and minigames would be called here, omitted for brevity
# e.g., mod_menu(), minigame_1(), minigame_2()

display_leaderboard()

st.markdown(
    """
    <br><br><center style="color:#00ff00;">Hacking simulation © 2024</center>
    """,
    unsafe_allow_html=True,
)
