import streamlit as st
import random
import json
import os

# --- Custom CSS for hacking green GUI and XP bar ---
st.markdown(
    """
    <style>
    /* Dark background and green neon text */
    .css-1d391kg {
        background-color: #000000;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Title styling */
    .css-1v0mbdj h1 {
        color: #00ff00;
        text-shadow: 0 0 10px #0f0, 0 0 20px #0f0;
        font-weight: bold;
        font-family: 'Consolas', Courier, monospace;
    }
    /* Buttons styling */
    div.stButton > button:first-child {
        background-color: black;
        color: #00ff00;
        border: 2px solid #00ff00;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        transition: background-color 0.3s, color 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #00ff00;
        color: black;
        cursor: crosshair;
    }
    /* Upgrade boxes */
    .upgrade-box {
        border: 1px solid #00ff00;
        padding: 10px;
        margin-bottom: 10px;
        font-family: 'Courier New', Courier, monospace;
        background-color: #001100;
        box-shadow: 0 0 8px #00ff00;
        border-radius: 5px;
    }
    /* Stats styling */
    .stats {
        font-family: 'Courier New', Courier, monospace;
        font-size: 18px;
        padding: 10px;
        background-color: #001a00;
        border: 1px solid #00ff00;
        box-shadow: 0 0 6px #00ff00;
        margin-bottom: 15px;
        border-radius: 5px;
        white-space: pre;
    }
    /* XP bar container */
    .xp-bar {
        position: relative;
        background-color: #003300;
        border: 1px solid #00ff00;
        border-radius: 5px;
        width: 100%;
        height: 25px;
        margin-bottom: 15px;
    }
    /* XP bar fill */
    .xp-bar-inner {
        background: linear-gradient(90deg, #00ff00, #00cc00);
        height: 100%;
        border-radius: 5px;
        transition: width 0.4s ease;
    }
    /* XP text overlay */
    .xp-text {
        position: absolute;
        width: 100%;
        text-align: center;
        top: 0;
        left: 0;
        color: black;
        font-weight: bold;
        line-height: 25px;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Mod menu box */
    .mod-menu-box {
        background-color: #002200;
        border: 1px solid #00ff00;
        padding: 15px;
        margin-top: 20px;
        border-radius: 5px;
        box-shadow: 0 0 10px #007700;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
        "max_level": 30,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

# --- Level up logic ---

def maybe_level_up():
    while st.session_state.level < st.session_state.max_level and st.session_state.xp >= st.session_state.xp_needed:
        st.session_state.xp -= st.session_state.xp_needed
        st.session_state.level += 1
        st.session_state.xp_needed = int(st.session_state.xp_needed * 1.5)
        st.success(f"🎉 Hacker Level UP! You are now Level {st.session_state.level}")

        if st.session_state.level >= 5:
            st.session_state.minigame1_unlocked = True
        if st.session_state.level >= 8:
            st.session_state.minigame2_unlocked = True
    
    # Cap XP at xp_needed if max level reached
    if st.session_state.level >= st.session_state.max_level:
        if st.session_state.xp > st.session_state.xp_needed:
            st.session_state.xp = st.session_state.xp_needed

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
    # Cap at 100% width when max level reached
    if st.session_state.level >= st.session_state.max_level:
        xp_percent = 100
    else:
        xp_percent = int((st.session_state.xp / st.session_state.xp_needed) * 100)
    bar_html = f"""
    <div class="xp-bar">
      <div class="xp-bar-inner" style="width: {xp_percent}%;"></div>
      <div class="xp-text">Level {st.session_state.level} — XP: {st.session_state.xp} / {st.session_state.xp_needed} ({xp_percent}%)</div>
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
    st.markdown(f'<div class="stats">{stats}</div>', unsafe_allow_html=True)
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
    if st.session_state.level < st.session_state.max_level:
        st.session_state.xp += 5
    maybe_level_up()
    if random.random() < st.session_state.password_drop_chance:
        st.session_state.passwords += 1
        st.toast("Password Cracked! +1 Password 🎁")
    game_update()

# --- Mod Menu with more features ---

def mod_menu():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🛠️ Mod Menu")

    if st.session_state.level < 3:
        st.info("Reach Hacker Level 3 to unlock the Mod Menu.")
        return

    # Feature 1: Brute Force Password (spends resources, gains passwords)
    if st.button("💻 Brute Force Password (Cost: 20 Crypto, 1 Password)"):
        if st.session_state.crypto >= 20 and st.session_state.passwords >= 1:
            st.session_state.crypto -= 20
            st.session_state.passwords -= 1
            gained = random.randint(2, 5)
            st.session_state.passwords += gained
            st.success(f"Brute Force successful! You cracked {gained} passwords.")
            st.session_state.xp += 15
            maybe_level_up()
            game_update()
        else:
            st.error("Not enough Crypto or Passwords for Brute Force.")

    # Feature 2: Firewall Override (Cost: 50 Crypto), temporary boost
    if st.session_state.level >= 5:
        if st.button("🛡️ Firewall Override (Cost: 50 Crypto)"):
            if st.session_state.crypto >= 50:
                st.session_state.crypto -= 50
                st.session_state.crypto_per_click += 20
                st.success("Firewall overridden! +20 Crypto per click temporarily.")
                st.session_state.xp += 20
                maybe_level_up()
                game_update()
            else:
                st.error("Not enough Crypto for Firewall Override.")

    # Feature 3: Password Sniffer (Level 10 unlock)
    if st.session_state.level >= 10:
        if st.button("📡 Password Sniffer (Cost: 100 Crypto, 5 Passwords)"):
            if st.session_state.crypto >= 100 and st.session_state.passwords >= 5:
                st.session_state.crypto -= 100
                st.session_state.passwords -= 5
                # Increase password drop chance significantly for next 20 clicks
                st.session_state.password_drop_boost_turns = 20
                st.success("Password Sniffer activated! +25% password drop chance for next 20 clicks.")
                st.session_state.xp += 30
                maybe_level_up()
                game_update()
            else:
                st.error("Not enough resources for Password Sniffer.")

# --- Track password drop boost turns and apply boost ---

def apply_password_drop_boost():
    if "password_drop_boost_turns" not in st.session_state:
        st.session_state.password_drop_boost_turns = 0
    if st.session_state.password_drop_boost_turns > 0:
        st.session_state.password_drop_chance_boosted = min(st.session_state.password_drop_chance + 0.25, 0.75)
        st.session_state.password_drop_boost_turns -= 1
    else:
        st.session_state.password_drop_chance_boosted = st.session_state.password_drop_chance

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

# --- Player name input with rerun ---

if "player_name" not in st.session_state or st.session_state.player_name == "":
    name = st.text_input("Enter your hacker handle (name):").strip()
    if name != "":
        st.session_state.player_name = name
        st.experimental_rerun()
    st.stop()
else:
    st.success(f"Welcome, {st.session_state.player_name}! Let's start hacking!")

# --- Main UI ---

st.title("🕵️‍♂️ Hacker Clicker: Crypto vs Firewall 🪙")

show_stats()

st.markdown("<hr>", unsafe_allow_html=True)

apply_password_drop_boost()  # Adjust password drop for boosts

if st.button("🪙 Hack Crypto"):
    # Use boosted password drop chance if boost is active
    actual_password_drop_chance = st.session_state.password_drop_chance_boosted
    st.session_state.crypto += st.session_state.crypto_per_click
    if st.session_state.level < st.session_state.max_level:
        st.session_state.xp += 5
    maybe_level_up()
    if random.random() < actual_password_drop_chance:
        st.session_state.passwords += 1
        st.toast("Password Cracked! +1 Password 🎁")
    game_update()

st.markdown("<hr>", unsafe_allow_html=True)

show_upgrades()

mod_menu()

st.markdown("<hr>", unsafe_allow_html=True)

display_leaderboard()

st.markdown(
    """
    <br><br><center style="color:#00ff00;">Hacking simulation © 2024</center>
    """,
    unsafe_allow_html=True,
)
